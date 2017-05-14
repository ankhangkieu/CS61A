.read lab12.sql

CREATE TABLE sp16favnum AS
  select number, count(*) as count from sp16students group by number order by count desc limit 1;

CREATE TABLE sp16favpets AS
  select pet, count(*) as count from sp16students group by pet order by count desc limit 10;

CREATE TABLE fa16favpets AS
  select pet, count(*) as count from students group by pet order by count desc limit 10;

CREATE TABLE fa16dragon AS
  select pet, count(*) as count from students where pet = "dragon" group by pet order by count;

CREATE TABLE fa16alldragons AS
  select "a dragon" as newpet, count(*) as count from students where pet like "%dragon%" group by newpet order by count;

CREATE TABLE obedienceimage AS
  select seven, denero, count(*) as count from students where seven = "7" group by denero order by denero;

CREATE TABLE smallest_int_count AS
  select smallest, count(*) as count from students where smallest >= 1 group by smallest order by smallest;
