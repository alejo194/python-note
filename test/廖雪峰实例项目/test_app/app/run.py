# import logging; logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from app.config import configs
from app.orm import create_pool
from app.web_framework import add_routes, add_static
from app import logger
from app.handlers import cookie2user, COOKIE_NAME


'''
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>')

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
'''

def init_jinja2(app, **kw):
    logger.info('init jinja2....')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )

    path = kw.get('path', None)

    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath('__file__')),'templates')
    logger.info('set jinja2 template path: %s' % path)
    # Environment是jinjia2中的一个核心类，它的实例用来保存配置、全局对象以及模板文件的路径
    env = Environment(loader = FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f

    app['__templating__'] = env

async def logger_factory(app, handler):
    async def logger_fact(request):
        logger.info('Request: %s %s' % (request.method, request.path))
        return await handler(request)
    return logger_fact

# 产生post提交的数据
# async def data_factory(app, handler):
#     async def parse_data(request):
#         if request.method == 'POST':
#             if request.content_type.startswith('application/json'):
#                 request.__data__ = await request.json()
#                 logger.info('request json: %s' % str(request.__data__))
#             elif request.content_type.startswith('application/x-www-form-urlencoded'):
#                 request.__data__ = await request.post()
#                 logger.info('request form: %s' % str(request.__data__))
#         return (await handler(request))
#     return parse_data
async def auth_factory(app, handler):
    async def auth(request):
        logger.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None

        cookie_str = request.cookies.get(COOKIE_NAME)
        # 获取到cookie字符串, cookies是用分号分割的一组名值对，在python中被看成dict
        if cookie_str:
            user = await cookie2user(cookie_str)
            # 通过反向解析字符串和与数据库对比获取出user
            if user:
                logger.info('set current user: %s' % user.email)
                request.__user__ = user
            # user存在则绑定到request上
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')

        # 继续执行下一步
        return (await handler(request))

    return auth

# 将url处理函数的返回值转换成response对象
async def response_factory(app, handler):
    async def response(request):
        logger.info('Response handler...')
        # 调用相应的URL处理请求
        r = await handler(request)
        logger.info('response result = %s' % str(r))
        # 如果响应结果为web.StreamResponse类（即URL处理函数直接返回web.Response）,则直接把它作为响应返回
        if isinstance(r, web.StreamResponse):
            return r
        # 如果响应结果为字节流，则把字节流塞到response的body里，设置响应类型为流类型，返回
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                # 先判断是不是需要重定向，是的话直接用重定向的地址重定向
                return web.HTTPFound(r[9])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            # 先查看一下有没有'__template__'为key的值
            template = r.get('__template__')
            if template is None:
                # 如果没有，说明要返回json字符串，则把字典转换为json返回，对应的response类型设为json类型
                resp = web.Response(body=json.dumps(
                        r, ensure_ascii=False, default=lambda o:o.__dict__).encode('utf-8'))
                resp.content_type='application/json'
                return resp
            else:
                r['__user__']=request.__user__
                # 在__base__.html中会根据__user__设置用户相关信息
                # 如果有'__template__'为key的值，则说明要套用jinja2的模板，'__template__'Key对应的为模板文件名
                # 得到模板文件然后**r去渲染render
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r <= 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            status_code, description = r
            # 如果tuple的第一个元素是int类型且在100到600之间，这里应该是认定为status_code为http状态码，description为描述
            if isinstance(status_code, int) and status_code >= 100 and status_code < 600:
                resp = web.Response(status=status_code, text=str(description))
                resp.content_type = 'text/plain;charset=utf-8'
                return resp
    return response

# 将blog评论的发布时间转换成多少时间以前
def datetime_filter(t):
    second_gap = int(time.time() - t)
    # time.time()取当前时间（新纪元开始后的秒数）
    if second_gap < 60:
        return u'1分钟前'
    if second_gap < 3600:
        return u'%s分钟前' % (second_gap // 60)
        # 双斜杠表示整除
    if second_gap < 86400:
        return u'%s小时前' % (second_gap // 3600)
    if second_gap < 604800:
        return u'%s天前' % (second_gap // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

async def init(loop):
    await create_pool(loop=loop, **configs.db)
    # middlewares(中间件)设置3个中间处理函数(都是装饰器)
    # middlewares中的每个factory接受两个参数，app 和 handler(即middlewares中的下一个handler)
    # 譬如这里logger_factory的handler参数其实就是auth_factory
    # middlewares的最后一个元素的handler会通过routes查找到相应的，其实就是routes注册的对应handler
    # 这其实是装饰模式的典型体现，logger_factory, auth_factory, response_factory都是URL处理函数前（如handler.index）的装饰功能
    app = web.Application(middlewares=[
        logger_factory, auth_factory, response_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    # 添加URL处理函数, 参数handlers为模块名
    add_routes(app, 'handlers')
    # 添加CSS等静态文件路径
    add_static(app)
    # 启动
    # srv = await loop.create_server(app.make_handler(), '0.0.0.0', 9000)
    # logger.info('server started at http://127.0.0.1:9000 ........')
    # return srv
    runner = web.AppRunner(app)
    await runner.setup()
    ite = web.TCPSite(runner, '0.0.0.0', 9000)
    logger.info('server started at http://0.0.0.0:9000 ........')
    await ite.start()



# 入口，固定写法
# 获取eventloop然后加入运行事件
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()