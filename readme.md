# ABN (Australian Business Number) Validator

Application that checks whether the ABNs in a provided spreadsheet are valid. If valid, a call will be made to the Australian Business Register (ABR) API to obtain the entity name and business name(s) associated with the ABN. Automates the task of manually verifying ABNs and searching the ABR website.

## Installation

**1. Clone _'abn_validator'_ Repository**</br></br>
HTML:

```
git clone https://github.com/Tomology/abn_validator.git
```

SSH:

```
git clone git@github.com:Tomology/abn_validator.git
```

GitHub CLI:

```
gh repo clone Tomology/abn_validator
```

**2. Create and Activate Virtual Environment**</br></br>
Create:

```
virtualenv env
```

Activate:

```
source env/Scripts/activate
```

**3. Install Dependencies**</br></br>
Change directories so you are in the folder that contains _requirements.txt_:

```
cd abn_validator
```

Install the project dependencies:

```
pip install -r requirements.txt
```

**4. Setup Secret Key**</br></br>
In _settings.py_ set the _SECRET_KEY_ variable to the location of your own secret key environment variable or generate one using [MiniWebTool](https://miniwebtool.com/django-secret-key-generator/).</br></br>
**5. Set DEBUG Value**</br></br>
In _settings.py_ set the _DEBUG_ value to _True_ or _False_.</br></br>
**6. Register for GUID**</br></br>
To be able to make calls to the ABR API you will need to register for a GUID. You can register for a GUID on the [ABR Website](https://abr.business.gov.au/Tools/WebServices).</br></br>
**7. Setup GUID**</br></br>
In the _utils.py_ file assign your GUID to the _guid_ variable.

```
guid = "your-guid-goes-here"
```

**8. Apply Migrations**</br></br>
Make sure you are located in the directory containing _manage.py_, then apply migrations:

```
python manage.py migrate
```

**9. Run Server**</br>

```
python manage.py runserver
```
