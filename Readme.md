### Toy Project

#### ERD (project) : 
```mermaid
erDiagram
    Users {
        id varchar
        password varchar
    }
    
    Posts {
        postId int
        title varchar
        content varchar
    }

```
#### Skills : <span style='color:gray'>Python, django, DRF(django rest framework)</span>

### Example :
#### How to run the server :
```sh
$ python3 ./manage.py runserver {ip:port}
```