# 2023-DB-Project
数据库课程项目作业-智慧安防小区系统  ![redis](https://img.shields.io/badge/qbdl-Intelligent--Security--Community-green2023)

前端Vue3,后端flask+mysql

基础前端模型参考的是Geeker-Admin https://github.com/HalseySpicy/Geeker-Admin 



## 一、使用说明

1、git clone https://github.com/qbdl/2023-DB-Project 

2、基础配置

- 前端（要安装一会会）:

  终端依次输入:

  - cd .\FrontEnd\
  - git init
  - npm install
  - npm run dev

- 后端: 直接运行2023-DB-Project\BackEnd\BackEnd_Routes.py应该就行（可能要安一些库倒是）



## 二、效果预览

![login1](./assets/login1.png)![home](./assets/home.png)

![datascreen](./assets/datascreen.png)

![personal_info_manage](./assets/personal_info_manage.png)

![community_info_manage](./assets/community_info_manage.png)

![info_import2](./assets/info_import2.png)

![vehicle_add](./assets/vehicle_add.png)

![release_announcement](./assets/release_announcement.png)

![image-20230506163634750](./assets/image-20230506163634750.png)

![car2](./assets/car2.png)



## 三、其他

- 如果想要继续开发的话，可以修改2023-DB-Project\FrontEnd\src\assets\json\dynamicRouter.json下的文件，这里面是不同的路由与页面（就是界面左边菜单显示的那些内容）
- mock数据来源修改的话在vite.config.js里server->proxy->target

- 一些没实现的功能：文件预览，图像更改，mock信息替换等😆
