// python3 -m http.server.

// To Adjust
boxWidth = 250;
lineWidth = 10;
offSet = 200
var mic;
var mySound;

var threshold = false;
var lastThreshold = false;
// sound input -> listen
// input below ~ -> say

function preload() {
  mySound = loadSound('bell.mp3');
}

function setup() {
  mySound.setVolume(0.7);
  mySound.play();
  frameRate(10)
  createCanvas(displayWidth, displayHeight);
  background(0)
  listen()
  // mic
  mic = new p5.AudioIn()
  mic.start();
}

function draw() {
   
   micLevel = mic.getLevel();
   
    if(micLevel) {
   	    console.log(micLevel)

	    if (micLevel > 20) {
	    	threshold = true
	    }
	   	else {
	   		threshold = false
	   	}
	   	if (lastThreshold != threshold && threshold) {
	   		mySound.play();
	   	}

   	 for ( var i = 0; i += 10; i < displayWidth)
       ellipse(i*10, constrain(height-micLevel*height*5, 0, height), 10, 10);
   }

    if(threshold) listen()
   	else say()
   	lastThreshold = threshold
}

function listen() {
  push()
  fill(0)
  stroke(245,166,35)
  strokeWeight(lineWidth)
  ellipse(displayWidth/2, displayHeight/2,1000,1000);
  ellipse(displayWidth/2, displayHeight/2,850,850);
  
  pop()
}

function say() {
  push()
  fill(0)
  stroke(245,166,35)
  strokeWeight(10)
  ellipse(displayWidth/2, displayHeight/2,1000,1000);
  rect(displayWidth/2-boxWidth/2, lineWidth, boxWidth ,boxWidth )
  rect(displayWidth/2-boxWidth/2-2*offSet, displayHeight-boxWidth-lineWidth-offSet, boxWidth ,boxWidth )
  rect(displayWidth/2-boxWidth/2+2*offSet, displayHeight-boxWidth-lineWidth-offSet, boxWidth ,boxWidth )

  fill(245,166,35)
  ellipse(displayWidth/2, displayHeight/2,100,100);
  pop()

}