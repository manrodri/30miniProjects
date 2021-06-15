const secondHand = document.querySelector('.second-hand');
const hourHand = document.querySelector('.hour-hand');
const minutesHand = document.querySelector('.min-hand');


function setDate(){
    const now = new Date();

    const seconds = now.getSeconds();
    const minutes = now.getMinutes();
    const hours = now.getHours();

    const minutesDegrees = ((minutes/60)*360) +90;
    const secondsDegrees = ((seconds/60) * 360) + 90;
    const hoursDegrees = ((hours/12)* 360) + 90;

    minutesHand.style.transform = `rotate(${minutesDegrees}deg)`;
    secondHand.style.transform = `rotate(${secondsDegrees}deg)`;
    hourHand.style.transform = `rotate(${hoursDegrees}deg)`
    console.log(secondHand.style.transform)

//    todo: fix weirdness when hands get to the 0deg trainsitiomn
//    this is due to rotate go 0 in the oposite direction. Fix it disabling temporary transform.
//    using if statements in the setDate function.
}

setInterval(setDate, 1000);