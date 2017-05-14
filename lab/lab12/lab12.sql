.read sp16data.sql
.read fa16data.sql

CREATE TABLE obedience AS
  select seven as obedience, denero from students;

CREATE TABLE smallest_int AS
  select time, smallest from students where smallest > 8 order by smallest limit 20;

CREATE TABLE greatstudents AS
  select a.date, a.number, a.pet, a.color, b.color from students as a, sp16students as b
          where a.date = b.date and a.number = b.number and a.pet = b.pet;

CREATE TABLE sevens AS
  select a.seven from students as a, checkboxes as b 
          where a.number = 7 and b."7" = "True" and a.time = b.time;
CREATE TABLE matchmaker AS
  select a.pet, a.song, a.color, b.color from students as a, students as b
          where a.time < b.time and a.pet = b.pet and a.song = b.song;
