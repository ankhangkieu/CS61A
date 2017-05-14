.read data.sql

-- Q1
create table flight_costs as
  with ticket(first, second, third, day) as(
    select 20, 30, 40, 1 union
    select second, third, (second+third)/2 + 5*((day+3)%7), day+1 from ticket where day < 25
  )
  select day, first from ticket;

-- Q2
create table schedule as
  with plan(flight, depart, arrive, cost, transit) as (
    select departure ||", "||arrival, departure, arrival, price, 0 from flights union
    select a.flight||", "||b.arrival, a.depart, b.arrival, a.cost+b.price, a.transit+1 from plan as a, flights as b 
          where a.arrive = b.departure and a.transit < 1
  )
  select flight, cost from plan where depart = "SFO" and arrive = "PDX" order by cost;

-- Q3
create table shopping_cart as
  with cart(things, curPrice, budget) as(
    select item, price, 60 - price from supermarket where price <= 60 union
    select a.things||", "|| b.item, b.price, a.budget - b.price from cart as a, supermarket as b 
          where a.budget >= b.price and a.curPrice <= b.price
  )
  select things, budget from cart order by budget, things;

-- Q4
create table number_of_options as
  select count(distinct meat) from main_course;

-- Q5
create table calories as
  select count(*) from main_course as a, pies as b where a.calories + b.calories < 2500;

-- Q6
create table healthiest_meats as
  select a.meat, min(a.calories + b.calories) from main_course as a, pies as b
        group by a.meat having max(a.calories + b.calories) <= 3000;

-- Q7
create table average_prices as
  select category, avg(MSRP) from products group by category;

-- Q8
create table lowest_prices as
  select item as item, store as store, price as price from inventory group by item having price = min(price);

-- Q9
create table shopping_list as
  select a.item as item, a.store as store from lowest_prices as a, products as b
         where a.item = b.name group by b.category having b.MSRP/b.rating = min(b.MSRP/b.rating);

-- Q10
create table total_bandwidth as
  select sum(a.Mbs) from stores as a, shopping_list as b where a.store = b.store;
