
function circles_total(id,value,maxValue,color1,clolor2){
    var myCircle = Circles.create({
        id:                  id,
        radius:              45,
        value:               value,
        maxValue:            maxValue,
        width:               7,
        text:                value+'人',
        colors:              [color1,clolor2],
        duration:            1000,
        wrpClass:            'circles-wrp',
        textClass:           'circles-text',
        valueStrokeClass:    'circles-valueStroke',
        maxValueStrokeClass: 'circles-maxValueStroke',
        styleWrapper:        true,
        styleText:           true
        });
}