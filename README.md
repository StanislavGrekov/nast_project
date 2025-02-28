## Блог самогонщика

### Описание процесса развертывания сайта на сервере:

- Создаем виртуальный сервер на REG.ru, при развертывании указываем публичный ключ SSH,
который мы (на текущей машине) либо находим командой ls -al ~/.ssh/ потом открываем (если ключ есть) командой nano  ~/.ssh/id_rsa.pub
или генерируем публичный ключ командрй ssh-keygen
- Создаем сервер, запускаем его, коннектимся к нему командой ssh root@85.123.123.25, вводим пароль который задали при
генерации публичного ключа
- Задаем нового пользователя 

        adduser virtualbox
- Добавляем его в группу админов 
  
      usermod virtualbox -aG sudo
- Переключаемся на пользователя 

        su virtualbox
- Обновляем пакетный менеджер 

        sudo apt update
- Устанавливаем программы 

        sudo apt install python3-pip python3-venv postgresql nginx
- Сразу задаем пользователю БД postgres новый пароль (такой же как в файле .env проекта), это делается чтобы не перенастраивать потом
т.е. заходим sudo su posgres, потом psql, потом ALTER USER postgres WITH PASSWORD "masterkey";

- создаем БД 

        CREATE DATABASE nast_db;
- клонируем проект из GIT в домашнюю директорию 

        git clone httpСсылка
- Создаем и активируем виртуальное окружение, устанавливаем пакеты из requirements.txt (проверяем чтоб в файле был Gunicorn)

        python3 -m venv venv 
        source venv/bin/activate
        pip install -r requirements.txt
- в проекте в файле requirements.txt проверяем чтоб был Dotenv, подключена созданная база, собрана статика
- делаем миграции и запускаем сервер для проверки

        python3 manage.py migrate
        python3 manage.py runserver 0.0.0.0:8000
- Запускаем nginx, проверяем его статус, заходим по ip адресу и видим его стартовую страницу

        sudo systemctl start nginx
        sudo systemctl status nginx
- Запускаем Гуникорн для поврерки командой и проверяем через браузер

        gunicorn nast_project.wsgi --bind 0.0.0.0:8000
        Проверяем ip_адрес:8000
- Настраиваем Gunicorn, для этого создаем файл:

        sudo nano /etc/systemd/system/gunicorn.service

        [Unit]
        Descriptio=Gunicorn service
        After=network.target
        
        [Service]
        User=virtualbox
        Group=www-data
        WorkingDirectory=/home/virtualbox/nast_project
        ExecStart=/home/virtualbox/nast_project/venv/bin/gunicorn --bind unix:/home/virtualbox/nast_project/nast_project/project.sock nast_project.wsgi:application --workers 3
        
        [Install]
        WantedBy= multi-user.target

- Запускаем Gunicorn и проверяем статус

        sudo systemctl restart gunicorn
        sudo systemctl status gunicorn
- Настраиваем Nginx, для этого создаем файл:

        sudo nano /etc/nginx/sites-available/my_project
        
        server {
                listen 80;
                server_name 95.163.231.21;
        
                location /static/ {
                        root /home/virtualbox/nast_project;
                }
                location / {
                        include proxy_params;
                        proxy_pass http://unix:/home/virtualbox/nast_project/nast_project/project.sock;
                }
        }

- Делаем сайт активным

        sudo ln -s /etc/nginx/sites-available/my_project /etc/nginx/sites-enable/
- Запускаем и проверяем статус nginx

        sudo systemctl restart nginx
        sudo systemctl status nginx
- Проверяем сайт по ip-адресу, НО у меня он не заработал, а заработал только тогда, когда я 
в конфигурационном файле Nginx сменил пользователя с www-data на virtualbox (какие-то проблемы с правами)

        cd /etc/nginx
        nano nginx.conf 
- Также имеет смысл проверить статику. В settings.py все настроенно верно, но статику можно пересобрать коммандой

        python3 manage.py collectstatic