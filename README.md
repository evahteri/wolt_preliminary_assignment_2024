# Solution for the Wolt Summer 2024 Engineering Internships backend assignment.

## Delivery Fee Calculator API

Add general info here

minimum_cart_value: 1000 #If the cart value is less than this, a small order surcharge is added to the delivery price (10€ = 1000).
minimum_delivery_distance: 500 #The minimum delivery fee as meters.
delivery_fee_for_the_first_km: 200 #The delivery fee for the first km.
additional_distance_after_first_km: 500 #The distance the courier has to travel after the first km, delivery_fee_for_additional_distance value is added for every additional distance.
delivery_fee_for_additional_distance: 100 #This is added to the delivery fee for every configured additional distance.
minimun_delivery_fee: 100 #The minimum delivery fee.
bulk_amount: 12 #Amount of products that is considered bulk.
bulk_charge_fee: 120 #This is added if the order is considered bulk.
product_amount_for_surcharge: 4 #Every product after this number has a surcharge fee.
surcharge_fee: 50 #This is added for every product after product_amount_for_surcharge.
max_delivery_fee: 1500 #The maximum delivery fee.
max_cart_value_for_free_delivery: 20000 #The maximum cart value for free delivery.
rush_hours: #The rush hours for the additional fee. Weekdays are 1-7, 1 is monday, 7 is sunday. Start and End times as UTC times, fee is a multiplier.
  - day: 5
    start: 15:00
    end: 19:00
    fee: 1.2

### Install

- Install requirements by runnin ```pip install -r requirements.txt```

### How to use

- Run the server in src folder with ```uvicorn main:app```

- You can configure the fee calculations by changing the config.json file:

```
minimum_cart_value: If the cart value is less than this, a small order surcharge is added to the delivery price (10€ = 1000).
minimum_delivery_distance: The minimum delivery fee as meters.
delivery_fee_for_the_first_km: The delivery fee for the first km.
additional_distance_after_first_km: The distance the courier has to travel after the first km, delivery_fee_for_additional_distance value is added for every additional distance.
delivery_fee_for_additional_distance: This is added to the delivery fee for every configured additional distance.
minimum_delivery_fee: The minimum delivery fee.
bulk_amount: Amount of products that is considered bulk.
bulk_charge_fee: This is added if the order is considered bulk.
product_amount_for_surcharge: Every product after this number has a surcharge fee.
surcharge_fee: This is added for every product after product_amount_for_surcharge.
max_delivery_fee: The maximum delivery fee.
max_cart_value_for_free_delivery: The maximum cart value for free delivery.
rush_hours: The rush hours for the additional fee. Weekdays are 1-7, 1 is monday, 7 is sunday. Start and End times as UTC times, fee is a multiplier.
  - day: 5
    start: 15:00
    end: 19:00
    fee: 1.2
```