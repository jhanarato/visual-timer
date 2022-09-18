# J.R.'s Visual Meditation Timer

I've created a meditation timer using [Pimoroni's Keybow2040](https://shop.pimoroni.com/products/keybow-2040) and Circuit Python. Tell all your deaf friends!

## Using the timer

The basic setup of the device is described on [Pimoroni's github page](https://github.com/pimoroni/pmk-circuitpython). Once you have the keyboard working you can copy the `meditation_timer.py` file to `code.py` on the device. If all goes well, the first thing you'll see are three buttons - red, green and blue.

![01-Minutes-Menu](https://user-images.githubusercontent.com/872786/190882966-d0f07cd8-c044-41d1-83ae-8b2452dda8a8.JPG)

This is what I call the "minutes menu". Each key represents a set number of minutes. 

- Red is 5 minutes
- Green is 10 minutes
- Blue is 15 minutes 

Press a key to choose. Your choice is displayed:

![02-Minutes-Chosen](https://user-images.githubusercontent.com/872786/190883260-e962775a-6136-4ed9-85a2-c46aeb2014f3.JPG)

Then you're taken to the "multiplier menu". This lets you choose a number between 1 and 16 to multiply the minutes by:

![03-Multiplier-Menu](https://user-images.githubusercontent.com/872786/190883361-641aedf3-22cb-4030-92d3-59eaba749f6e.JPG)
![04-Multiplier-Chosen](https://user-images.githubusercontent.com/872786/190883376-1502ba35-d7e0-442d-a8be-369331345cc6.JPG)

We first chose green (10 minutes) and then a multiplier of 10, so the timer will now run for 100 minutes.

To reassure us that the timer is running, a single orange key is lit:

![05-Timer-Running-Indicator](https://user-images.githubusercontent.com/872786/190883401-69f7e36f-bfca-45b0-b962-92948f932828.JPG)

While the timer is running, we can select from 4 views, including the indicator above. Press any key to go to the next view. The next two views show the minutes & multiplier selection as shown above.

The countdown indicator starts by showing us all green keys.

![06-Countdown-Beginning](https://user-images.githubusercontent.com/872786/190883447-26c3b58f-a6ea-43d0-8004-6e7ca6a51a56.JPG)

As the countdown progresses, keys turn from green to blue one by one:

![07-Countdown-Running](https://user-images.githubusercontent.com/872786/190883468-c898e357-b6ae-48ec-abde-527ff588d1b0.JPG)

One more click takes us back to the single key indicator. You can cycle through the views as many times as you like.

A long press at any time will take you back to the minutes menu.

Finally, when the timer is finished, all keys light up orange:

![08-Time-Up](https://user-images.githubusercontent.com/872786/190883541-73b66e04-9ebe-49cd-86e8-7b284364919e.JPG)

A single click takes you back to the minutes menu.
