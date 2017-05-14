create table parents as
  select "abraham" as parent, "barack" as child union
  select "abraham"          , "clinton"         union
  select "delano"           , "herbert"         union
  select "fillmore"         , "abraham"         union
  select "fillmore"         , "delano"          union
  select "fillmore"         , "grover"          union
  select "eisenhower"       , "fillmore";

create table dogs as
  select "abraham" as name, "long" as fur, 26 as height union
  select "barack"         , "short"      , 52           union
  select "clinton"        , "long"       , 47           union
  select "delano"         , "long"       , 46           union
  select "eisenhower"     , "short"      , 35           union
  select "fillmore"       , "curly"      , 32           union
  select "grover"         , "short"      , 28           union
  select "herbert"        , "curly"      , 31;

create table sizes as
  select "toy" as size, 24 as min, 28 as max union
  select "mini",        28,        35        union
  select "medium",      35,        45        union
  select "standard",    45,        60;

-------------------------------------------------------------
-- PLEASE DO NOT CHANGE ANY SQL STATEMENTS ABOVE THIS LINE --
-------------------------------------------------------------

-- The size of each dog
create table size_of_dogs as
  select name, size from dogs, sizes where height >= min and height <=max group by name;

-- All dogs with parents ordered by decreasing height of their parent
create table by_height as
  select child from parents, dogs where parent = name order by -height;

-- Sentences about siblings that are the same size
create table sentences as
  with siblings(first, second, size) as(
    select a.child, b.child, c.size from parents as a, parents as b, size_of_dogs as c, size_of_dogs as d
          where a.child < b.child and a.parent = b.parent and a.child = c.name 
                and b.child = d.name and c.size = d.size
  )
  select first || " and " || second || " are "||size|| " siblings" from siblings;

-- Ways to stack 4 dogs to a height of at least 170, ordered by total height
create table stacks as
  select a.name||", "|| b.name ||", "|| c.name ||", "|| d.name, a.height+b.height+c.height+d.height as total
      from dogs as a, dogs as b, dogs as c, dogs as d
        where a.height<b.height and b.height<c.height and c.height< d.height
              and a.height+b.height+c.height+d.height >= 170 order by total;

-- non_parents is an optional, but recommended question
-- All non-parent relations ordered by height difference
create table non_parents as
  with grand(gparent, gchild) as(
    select a.parent, b.child from parents as a, parents as b where a.child = b.parent 
  )
  select a.parent, b.child from grand as g, parents as a, parents as b, dogs as c, dogs as d 
    where (a.parent = g.gparent or a.child = g.gparent) and (b.parent = g.gchild or b.child = g.gchild) and
          a.parent = c.name and b.child = d.name order by (c.height - d.height);

create table ints as
    with i(n) as (
        select 1 union
        select n+1 from i limit 100
    )
    select n from i;

create table divisors as
    select a.n as num, count(*) as count from ints as a, ints as b where a.n%b.n = 0 group by a.n;

create table primes as
    select num from divisors where count = 2;
