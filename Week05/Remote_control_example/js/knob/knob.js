// Knob
$(function () {
    // Init vars
    var knobs = $('.knob-container');
    var knobVal = [];
    knobVal.length = knobs.length;

    // Init knob appearance
    knobs.knobKnob({
        startDeg: -45,
        degRange: 270,
        initVal: 0.0,
        numColorbar: 31,
    });

    // Check knob val updated or not
    function knobChecker() {
        // Check update
        for(var i=0; i<knobs.length; ++i)
            if( knobVal[i] !== $(knobs[i]).val() ) {
                knobVal[i] = $(knobs[i]).val().toString();
                csmapi.push('IoTtalk_Control_Panel', '',$(knobs[i]).attr('role'), [parseFloat(knobVal[i])]);
            }
    }
    setInterval(knobChecker, 250);
});