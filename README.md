<h1 align="center">
Hi there, it is API project Mountain Map!
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/>
</h1>
<h3 align="center">See below all functionality of API </h3>

Swagger API Documentation - https://app.swaggerhub.com/apis/KAITMEN17/PerevalAPI/1.0.0

<hr>
<h3>Short API description</h3>
GET: /api/submit_data  --  get all perevals <br>
POST: /api/submit_data  --  create new pereval

GET: /api/submit_data/?user__email=example@gmail.com  --  get all perevals of user example@gmail.com <br>
GET: /api/submit_data/id  --  get detail pereval by id <br>

PUT: /api/submit_data/id  --  edit pereval by id (all info except user detail) <br>


<h1 align="center">Are you developer and want use project on local server?</h1>
<h3 align="center">Follow next steps:</h3>
<hr>
1. Create project in Pycharm with name as you like<br>
2. In terminal enter ```git clone https://github.com/kaitmen/MountainMap```<br>
3. In terminal enter ```cd *project name*```<br>
4. In terminal enter ```pip install -r requirements.txt```<br>
5. Open settings.py file and make database configurations<br>
6. In terminal enter ```python manage.py makemigrations```<br>
7. In terminal enter ```python manage.py migrate```<br>
8. In terminal enter ```python manage.py runserver```<br>

Now you can testing API


