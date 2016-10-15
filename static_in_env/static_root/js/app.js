var durations = [];

$(document).ready(function(){

   $('.slideshow ').cycle({
      fx:     'fade',
      speed:  'fast',
      timeoutFn: computeTimeout
   });

   function calculateTimeout(currElement, nextElement, opts, isForward) {
      var index = opts.currSlide;
      return durations[index];
   }
});