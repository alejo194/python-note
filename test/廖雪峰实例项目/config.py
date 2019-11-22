import yaml, os, sys, codecs, logging
#去执行语句中.yml文件 -- python run.py /etc/conf/config.yml
# for pa in sys.argv:
#     if pa.endswith(".yml"):
#         cfg_file = pa
#         break
# else:
#     raise Exception("the args is not container config.yml ")

# load当前目录下.yml 文件
for file in os.listdir():
    if file.endswith(".yml"):
        cfg_file = file
        break
else:
    raise Exception("not find '*.yml' file!")
## load config yaml.load 把其变成字典
config = yaml.load(codecs.open(cfg_file,'r',encoding='UTF-8'))
logger_level = config['logger_level']
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger.setLevel(logger_level)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

