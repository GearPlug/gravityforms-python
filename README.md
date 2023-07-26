# gravityforms-python
![](https://img.shields.io/badge/version-0.1.0-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*gravityforms-python* is an API wrapper for Gravityforms (Wordpress plugin), written in Python.  
This library uses Oauth1 for authentication.
## Installing
```
pip install gravityforms-python
```
## Usage
```python
from gravityforms.client import Client
client = Client(base_url, consumer_key, consumer_secret)
```
### List Entries
```python
entries = client.list_entries()
```
### Filter entries
```python
entries = client.filter_entries(filter_field, filter_value, filter_operator, sorting_direction=None, page_size=None)
```
### List Forms
```python
forms = client.list_forms()
```
### Get Form detail
```python
form = client.get_form_detail(form_id)
```
