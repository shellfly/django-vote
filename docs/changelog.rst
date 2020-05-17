Changelog
=========

2.2.0 (2020.05.20)
------------------
* Add post_vote signal
* Add VoteMixin for easily write vote api
* Drop support for Django < 2.0
* Add Django 3.0 test

2.1.7(2018.05.08)
-----------------
* fix template tag error on Django 2.0

2.1.6(2017.12.20)
------------------

 * fix error on Django 2.0

2.1.5(2017.10.08)
------------------

* rename user_vote to get


2.1.4(2017.02.09)
------------------

* Support vote down


2.1.2(2016.11.02)
------------------

* Add missing migration files
* add more tests

2.0.0(2016.07.15)
-----------------
* use user_id on vote model, Drop support for Django < 1.7

1.1.3(2016.03.17)
-----------------
 * fix decrease to negative bug

1.1.1(2015.12.11)
-----------------
 * Python 3 support

1.1.0(2015.11.12)
-----------------
 * add api `all`, return all instances voted by specify user.

1.0.9(2015.09.24)
-----------------
 * add extra field. When up and down, the extra field on parasite model will be updated

1.0.5(2014.07.09)
-----------------
 * change default order_by to '-id' 

1.0.4(2014.07.09)
-----------------
 * enable using custom field name for VotableManager
 * fix empty queryset bug

1.0.3 (2014.07.08)
-----------------
 * add compat code  

1.0.2 (2014.07.08)
-----------------
 * add unit test

1.0 (2014.07.07)
----------------
