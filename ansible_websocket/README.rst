说明
*******

本例子用于演示在开发ansible API应用时，
使用websocket来通知WEB前端ansible playbook任务的执行情况

涉及的知识点:

1.  tornado的websocket开发
2.  flask与tornado的整合
3.  ansible callback plugins开发
4.  静态方法(@staticmethod)和类方法(@classmethod)


运行
======
1.  运行http server `python ansible_example.py`
2.  在浏览器中打开页面，建立websocket连接
3.  运行ansible-playbook `cd op && ansible-playbook -i inventory production.yml -k`
