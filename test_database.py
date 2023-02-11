# zeitatea@zeitatea-G551JW:~$ sudo -i -u postgres
# postgres@zeitatea-G551JW:~$ psql
# psql (14.6 (Ubuntu 14.6-0ubuntu0.22.04.1))
# Type "help" for help.

# postgres=# create database project_tracker;
# CREATE DATABASE
# postgres=# \l
# After execution:
#postgres=# \c project_tracker 
# You are now connected to database "project_tracker" as user "postgres".
# project_tracker=# select * from projects;

from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
####!!!!! The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base()
from sqlalchemy.orm import declarative_base
# import psycopg2

engine=create_engine("postgresql://postgres:password@localhost:5432/projectnou")
Base=declarative_base()

class Project(Base):
    __tablename__="projects"

    project_id=Column(Integer,primary_key=True)
    title=Column(String(length=50))

    def __repr__(self):
        return "<Project(project_id'{0}',title='{1}')>".format(self.project_id,self.title)


class Task(Base):
    __tablename__="tasks"

    task_id=Column(Integer,primary_key=True)
    project_id=Column(Integer,ForeignKey("projects.project_id"))
    description=Column(String(length=50))

    project=relationship("Project")

    def __repr__(self):
        return "<Task(description'{0}')>".format(self.description)

Base.metadata.create_all(engine)

def create_session():
    sesssion=sessionmaker(bind=engine)
    return sesssion()

if __name__=="__main__":
    session=create_session()
    clean=Project(title="Clean House")
    session.add(clean)
    session.commit()

    task=Task(description="Clean bedroom",project_id=clean.project_id)
    session.add(task)
    session.commit()