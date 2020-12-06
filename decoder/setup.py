from setuptools import setup, find_packages  

setup(  
    name = "DAVS3_Python",
    version = "1.0",  
    keywords = ("AVS3"),  
    description = "AVS3 decoder achieved by Python",  
    long_description = "AVS3 decoder achieved by Python",  
    license = "MIT Licence",  
    url = "https://github.com/zhangjinrong/AVS_python",  
    author = "ZhangJinrong",  
    author_email = "solrong@qq.com",  
    packages = find_packages(),  
    include_package_data = True,  
    platforms = "any",  
    install_requires = [],  
    scripts = [],  
    entry_points = {  
        'console_scripts': [  
            'test = test.help:main'  
        ]  
    }
)