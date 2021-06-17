window.onload = function() {
  setTimeout(function () {
      location.reload()
  }, 300000);
};

if ('serviceWorker' in navigator && 'caches' in window) {
  navigator.serviceWorker.register('./service-worker.min.js', {scope: './'} ).then(
      (reg) => {
        // registration worked
        console.log('Registration succeeded. Scope is ' + reg.scope);
        //// Clean expired tiles from the cache at startup
        reg.active.postMessage(JSON.stringify({action: 'PURGE_EXPIRED_TILES'}));
      }
  ).catch((error) => {
      console.log(`Registration failed with ${error}.`);
  });
}

var apiUrl = "http://127.0.0.1:8000"

// ####################################
// # replaces content of specified DIV
// ####################################
function printToDivWithID(id,text){
  div = document.getElementById(id);
  div.innerHTML += text;
}

function cleanDivWithID(id){
  div = document.getElementById(id);
  div.innerHTML = "";
}

function OnClickLinkDetails(source_name, target_name, source_interfaces, target_interfaces ){
    cleanDivWithID("infobox")
    cleanDivWithID("infobox_header")

    printToDivWithID("infobox_header", source_name.id + " - " + target_name.id + "<br>")

    targetdiv = document.getElementById("infobox")

    fetch(apiUrl + "/stats/?q=" + source_name.id + "&q=" + target_name.id)
    .then(function(response) {
        if (response.status !== 200) {
          throw new Error('Looks like there was a problem. Status Code: ' + response.status);
        }
        return response.json();
    }).then(function(data){
          for (var iface of source_interfaces){

              var interface = data[source_name.id][iface];
              var iDivGraph = document.createElement('div');
              iDivGraph.id = source_name.id + "_" + interface['ifDescr'] + "_graph";
              targetdiv.appendChild(iDivGraph);

              draw_device_interface_graphs_to_div(interface,source_name.id, targetdiv)
          }
          for (var iface of target_interfaces){
              var interface = data[target_name.id][iface];
              var iDivGraph = document.createElement('div');
              iDivGraph.id = target_name.id + "_" + interface['ifDescr'] + "_graph";
              targetdiv.appendChild(iDivGraph);

              draw_device_interface_graphs_to_div(interface, target_name.id, targetdiv)
          }

    })
    .catch(function(err) {
      console.log('Fetch Error :-S', err);
    });
}

// ###################################
// # Graph Drawing Functions         #
// ###################################

// This draws a single specific interface to div
function draw_device_interface_graphs_to_div(interfaceName, deviceid, targetdiv){

        var iDiv = document.createElement('div');
        iDiv.id = deviceid + "_" + interfaceName['ifDescr'] + "_graph_header";
        iDiv.align = 'left';
        iDiv.innerHTML = "<br>" + deviceid + " - " + interfaceName['ifDescr'];
        targetdiv.appendChild(iDiv);

        var iDivGraph = document.createElement('div');
        iDivGraph.id = deviceid + "_" + interfaceName['ifDescr'] + "_graph";
        targetdiv.appendChild(iDivGraph);
        var TimeStampStrings = []
        var InOctetsData = []
        var OutOctetsData = []

        for (var stats of interfaceName['stats']){
            TimeStampStrings.push(stats['time'])
            InOctetsData.push(stats['InSpeed'])
            OutOctetsData.push(stats['OutSpeed'])
        }

        draw_graph_from_data_to_div(InOctetsData,OutOctetsData,TimeStampStrings,iDivGraph)

}

// This draws all interfaces from device to div
function draw_device_graphs_to_div(deviceid, data, targetdiv){

    for (var interface of data[deviceid]['interfaces']){
        draw_device_interface_graphs_to_div(interface,deviceid, targetdiv)
    }
}


function draw_graph_from_data_to_div(InOctetsData,OutOctetsData,TimeStampStrings,iDivGraph){

    var selectorOptions = {
      buttons: [
      {
          step: 'day',
          stepmode: 'todate',
          count: 1,
          label: '1d'
      }, {
          step: 'day',
          stepmode: 'todate',
          count: 3,
          label: '3d'
      }, {
          step: 'day',
          stepmode: 'todate',
          count: 7,
          label: '1w'
      }, {
          step: 'month',
          stepmode: 'todate',
          count: 1,
          label: '1m'
      }, {
          step: 'month',
          stepmode: 'todate',
          count: 3,
          label: '3m'
      }, {
          step: 'month',
          stepmode: 'todate',
          count: 6,
          label: '6m'
      }, {
          step: 'year',
          stepmode: 'todate',
          count: 1,
          label: '1y'
      }, {
          step: 'all',
      }],
    };

    traceOut = {
      type: 'scatter',
      x: TimeStampStrings,
      y: OutOctetsData,
      mode: 'lines',
      name: 'Out',
      line: {
        color: 'rgb(219, 64, 82)',
        width: 3
      }
    };

    traceIn = {
      type: 'scatter',
      x: TimeStampStrings,
      y: InOctetsData,
      mode: 'lines',
      name: 'In',
      line: {
        color: 'rgb(55, 128, 191)',
        width: 3
      }
    };

    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    var layout = {
      color: '#fff',
      margin: {
        //autoexpand: true,
        l: 35,
        r: 20,
        t: 5,
        b: 35
      },
      width: 600,
      height: 350,
      xaxis: {
        title: 'Time',
        //showgrid: true,
        zeroline: true,
        showline: true,
        //linecolor: '#fff',
        rangeselector: selectorOptions,
        rangeslider: {},
        autorange: false,
        range: [yesterday, today],
        type: "date"
      },
      yaxis: {
        title: 'bps',
        showline: true,
        //linecolor: '#fff',
        showtickprefix: 'first'
      },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)'
    };

    var data = [traceOut, traceIn];

    var config = {
      toImageButtonOptions: {
        format: 'svg', // one of png, svg, jpeg, webp
        filename: 'traffic',
        height: 250,
        width: 600,
        scale: 1 // Multiply title/legend/axis/canvas sizes by this factor
      },
      modeBarButtonsToRemove:['sendDataTocloud', 'zoomIn2d', 'zoomOut2d','autoScale2d','resetScale2d','resetViewMapBox','resetViews'],
      displaylogo: false,
      responsive: true
    };

    //Plotly.newPlot(iDivGraph, data, layout, {showSendToCloud: false});
    console.time('Draw_device_iface')
    //Plotly.react(iDivGraph, data, layout, config);
    Plotly.react(iDivGraph, data, layout, config);
    console.timeEnd('Draw_device_iface')
}


// =============================
// PRINTING DEVICE DETAILS TABLE
// =============================

function viewChangeFunc(deviceid) {
    var selectBox = document.getElementById("viewSelectBox");
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;
    OnViewChange(deviceid,selectedValue);
}

function OnClickDetails(deviceid, view = "neighbors"){
    cleanDivWithID("infobox_header")
    printToDivWithID("infobox_header",deviceid);
    view_select_box = ""
    view_select_box += "<div>views: <select id=\"viewSelectBox\" onchange=\"viewChangeFunc(\'"+deviceid+"\');\">"
    view_select_box += "<option value=\"neighbors\">Neighbors</option>"
    view_select_box += "<option value=\"traffic\">Traffic</option>"
    view_select_box += "<option value=\"clear\">Clear</option>"
    view_select_box += "</select></div><br>"
    printToDivWithID("infobox_header",view_select_box)

    // ## INITIATE FIRST PASSIVE VIEW CHANGE
    OnViewChange(deviceid)
}

function OnViewChange(deviceid, view = "neighbors"){
    // # Initial cleanup
    cleanDivWithID("infobox")

    // #############################
    // # CREATING GRAPHS      #
    // #############################
    if (view == "traffic"){
        fetch(apiUrl + "/stats/?q=" + deviceid)
        .then(
          function(response) {
            if (response.status !== 200) {
              console.log('Looks like there was a problem. Status Code: ' +
                response.status);
              return;
            }
            response.json().then(function(data) {

              for (var iface in data[deviceid]) {
                var interface = data[deviceid][iface]
                var targetdiv = document.getElementById("infobox")
                var iDivGraph = document.createElement('div');
                iDivGraph.id = deviceid + "_" + interface['ifDescr'] + "_graph";
                targetdiv.appendChild(iDivGraph);
                draw_device_interface_graphs_to_div(interface, deviceid, iDivGraph)
              }
            });
          }
        )
        .catch(function(err) {
          console.log('Fetch Error :-S', err);
        });
    }
    // #############################
    // # READING NEIGHBORS VIEW    #
    // #############################
    else if (view == "neighbors"){
        fetch(apiUrl + "/neighborships/?q=" + deviceid)
        .then(
          function(response) {
            if (response.status !== 200) {
              console.log('Looks like there was a problem. Status Code: ' +
                response.status);
              return;
            }
            response.json().then(function(data) {
              if (data.length !== 0) { 
                  printToDivWithID("infobox",tableFromNeighbor(data));
              }
              else {
                warning_text = "<h4>The selected device id: ";
                warning_text+= deviceid;
                warning_text+= " is not in database!</h4>";
                warning_text+= "This is most probably as you clicked on edge node ";
                warning_text+= "that is not SNMP data gathered, try clicking on its neighbors.";
                printToDivWithID("infobox",warning_text);
              }
            });
          }
        )
        .catch(function(err) {
          console.log('Fetch Error :-S', err);
        });
    } else if (view == "clear"){
      cleanDivWithID("infobox");
      //cleanDivWithID("infobox_header")
    };
}

// ####################################
// # using input parameters returns
// # HTML table with these inputs
// ####################################
function tableFromUnusedInterfaces(key,data){
  text = "<table class=\"infobox2\">";
  text+= "<thead><th>LOCAL INT.</th><th>TYPE</th><th>SPEED</th>";
  text+= "</thead>";

  for (var neighbor in data[key]) {
    text+= "<tr>";

    //console.log("local_intf:" + data[key][neighbor]['ifDescr']);
    text+= "<td>" + data[key][neighbor]['ifDescr'] + "</td>";
    //console.log("description:" + data[key][neighbor]['ifType']);
    text+= "<td>" + data[key][neighbor]['ifType'] + "</td>";
    //console.log("actual_bandwith:" + data[key][neighbor]['ifSpeed']);
    text+= "<td>" + data[key][neighbor]['ifSpeed'] + "</td>";

    text+= "</tr>";
  }

  text+= "</table>";

  return text;
}

// ####################################
// # using input parameters returns
// # HTML table with these inputs
// ####################################
function tableFromNeighbor(data){
  text = "<table class=\"infobox\">";
  text+= "<thead><th>LOCAL INT.</th><th>NEIGHBOR</th><th>NEIGHBOR'S INT</th>";
  text+= "</thead>";

  for (let neighbor of data) {
    text+= "<tr>";

    //console.log("local_intf:" + neighbor['local_intf']);
    text+= "<td>" + neighbor['local_intf'] + "</td>";
    //console.log("neighbor_intf:" + neighbor['neighbor_intf']);
    text+= "<td>" + neighbor['neighbor'] + "</td>";
    //console.log("neighbor:" + neighbor['neighbor']);
    text+= "<td>" + neighbor['neighbor_intf'] + "</td>";

    text+= "</tr>";
  }

  text+= "</table>";

  return text;
}

// #######################################
// ########### NAV BUTTONS ###############
// #######################################
document.getElementById("down-button").addEventListener("mousedown", navDownFunctionClick);
document.getElementById("down-button").addEventListener("mouseup", navRelease);
document.getElementById("up-button").addEventListener("mousedown", navUpFunctionClick);
document.getElementById("up-button").addEventListener("mouseup", navRelease);
document.getElementById("left-button").addEventListener("mousedown", navLeftFunctionClick);
document.getElementById("left-button").addEventListener("mouseup", navRelease);
document.getElementById("right-button").addEventListener("mousedown", navRightFunctionClick);
document.getElementById("right-button").addEventListener("mouseup", navRelease);

document.addEventListener("mouseup", navRelease);
document.addEventListener("mouseout", navRelease);

// ########### VARIABLES #################
var MouseDownID = -1;
var x_trans = 0
var y_trans = 0

// ########### TRANSFORM FUNCTION ########
// Change element attribute
function transform_delta(delta_x,delta_y){
	var nodes_g = document.getElementById('nodes-g');
	var links_g = document.getElementById('links-g');
	//console.log("Current transforms: " + x_trans + ":" + y_trans)
	x_trans = x_trans + delta_x
	y_trans = y_trans + delta_y
	//console.log("New transforms: " + x_trans + ":" + y_trans)
	nodes_g.setAttribute("transform", "translate(" + x_trans + "," + y_trans +")")
	links_g.setAttribute("transform", "translate(" + x_trans + "," + y_trans +")")
}

// ########### DOWN BUTTON ###############
function navDownFunctionClick() {
  document.getElementById("down-button").style["color"] = "red";
  //console.log("navDownFunctionClick")
  if(MouseDownID==-1)  //Prevent multimple loops!
     MouseDownID = setInterval(WhileNavDownMouseDown, 100 /*execute every 100ms*/);
}
function WhileNavDownMouseDown() {
   //console.log("WhileNavDownMouseDown")
   transform_delta(0,10)
}

// ########### UP BUTTON ###############
function navUpFunctionClick() {
  document.getElementById("up-button").style["color"] = "red";
  //console.log("navUpFunctionClick")
  if(MouseDownID==-1)  //Prevent multimple loops!
     MouseDownID = setInterval(WhileNavUpMouseDown, 100 /*execute every 100ms*/);
}
function WhileNavUpMouseDown() {
   //console.log("WhileNavUpMouseDown")
   transform_delta(0,-10)
}
// ########### LEFT BUTTON ###############
function navLeftFunctionClick() {
  document.getElementById("left-button").style["color"] = "red";
  //console.log("navLeftFunctionClick")
  if(MouseDownID==-1)  //Prevent multimple loops!
     MouseDownID = setInterval(WhileNavLeftMouseDown, 100 /*execute every 100ms*/);
}
function WhileNavLeftMouseDown() {
   //console.log("WhileNavLeftMouseDown")
   transform_delta(-10,0)
}

// ########### RIGHT BUTTON ###############
function navRightFunctionClick() {
  document.getElementById("right-button").style["color"] = "red";
  //console.log("navRightFunctionClick")
  if(MouseDownID==-1)  //Prevent multimple loops!
     MouseDownID = setInterval(WhileNavRightMouseDown, 100 /*execute every 100ms*/);
}
function WhileNavRightMouseDown() {
   //console.log("WhileNavRightMouseDown")
   transform_delta(10,0)
}


// ########### COMMON RELEASE BUTTON ###############
function navRelease() {
  //console.log("navRelease")
  document.getElementById("down-button").style["color"] = "black";
  document.getElementById("up-button").style["color"] = "black";
  document.getElementById("left-button").style["color"] = "black";
  document.getElementById("right-button").style["color"] = "black";
  clearInterval(MouseDownID)
  MouseDownID = -1;
}

// ###########################
// RESIZE SVG ON WINDOW RESIZE
// ###########################

var intervalID = setInterval(resize_svg_on_window_resize, 5000);
function resize_svg_on_window_resize(){
    //console.log("resize_svg_on_window_resize TRIGGERED")
    var svg_element = document.getElementById('primary-svg');
    var original_viewBox = svg_element.getAttribute("viewBox")
    var res = original_viewBox.split(" ");

    // ### SELECT EITHER LEFT SIDEBAR OR WINDOW AS THE NEW HIGHT WHICHEVER IS BIGGER
    windowHeight = window.innerHeight; //|| document.documentElement.clientHeight || document.body.clientHeight;
    var rect = document.getElementById('left-sidebar').getBoundingClientRect();

    if (rect.height > windowHeight){
        var newClientHeight = rect.height;
    } else {
        var newClientHeight = windowHeight;
    }

    // ### SET THE HIGHT OF THE SVG AND SURROUNDING CONTAINER
    //console.log("new height: " + newClientHeight)
    svg_element.setAttribute("viewBox", res[0] + " " + res[1] + " " + res[2] + " " + newClientHeight)
    // Trying to set height of main SVG
    document.getElementById('container').style.height = newClientHeight + "px";

    slider_input()
}


// ########
// # MAIN #
// ########

// #################################
var svg = d3.select("div#container")
    .append("svg")
    .attr("id", "primary-svg")
    .attr("preserveAspectRatio", "xMinYMin")
    .attr("viewBox", "0 0 6000 6000")
    //.attr("viewBox", [0, 0, width, height])
    .classed("svg-content", true);



var svg_element = document.getElementById('primary-svg');
var positionInfo = svg_element.getBoundingClientRect();
    height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    width = positionInfo.width ;
    svg_element.setAttribute("preserveAspectRatio", "xMinYMin")
    svg_element.setAttribute("viewBox", "0 0 " + width + " " + height)
    //console.log("Initial width:" + width)
    //console.log("Initial height:"+ height)

// Trying to set height of main SVG
document.getElementById('container').style.height = height + "px";

// ###########  Scale Slider controls ##########
var slider = document.getElementById("scale_slider");
var output = document.getElementById("scale_indicator");
output.value = width
output.innerHTML = width;
initial_scale = width

slider.addEventListener("input", slider_input);

function slider_input() {
  var slider = document.getElementById("scale_slider");

  output.innerHTML = slider.value;
  //console.log("Scale_input: " + slider.value)

  // Change element attribute
  var svg_element = document.getElementById('primary-svg');
  var original_viewBox = svg_element.getAttribute("viewBox")
  var res = original_viewBox.split(" ");
  res[0] = (initial_scale - slider.value) / 2
  wh_ratio = ( (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight) / initial_scale )
  res[1] = wh_ratio + res[0] * wh_ratio
  //console.log("view X: " + res[0] + " view Y: " + res[1])
  svg_element.setAttribute("viewBox", res[0] + " " + res[1] + " " + slider.value + " " + slider.value)
}

// ###########  FORCE Slider controls ##########
var force_slider = document.getElementById("force_slider");
var force_output = document.getElementById("force_indicator");
force_output.value = 100
//console.log("Force_output.value:" + force_output.value)
force_output.innerHTML = force_output.value;

force_slider.oninput = function() {
  force_output.innerHTML = this.value;
  //console.log("force_output: " + this.value)

  simulation.force("y", d3.forceY(height/2).strength(this.value / 1000))  //### PARAMETRIZED FORCE TO SLIDER
  //console.log("starting simulation");
  simulation.alphaTarget(0.03).restart()
  simulation.alpha(1).restart()
  //delay
  setTimeout(function(){ simulation.alphaTarget(0); /*console.log("Ending simulation");*/ }, "1000")
}

// ##### GRAPH POPULATION #######
var color = d3.scaleOrdinal(d3.schemeCategory10);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id }).distance(100).strength(0.001))
    .force("charge", d3.forceManyBody().strength(-200).distanceMax(500).distanceMin(150))
    .force("x", d3.forceX(function(d){ return (d.group * width * 0.7 / 6)}).strength(1))
    .force("y", d3.forceY(height/2).strength(force_output.value / 1000))  //### PARAMETRIZED FORCE TO SLIDER
    .force("center", d3.forceCenter(width * 2/3, height / 2))
    .force("collision", d3.forceCollide().radius(25));

// #########################################
// # Get graph from api and draw SVG graph #
// #########################################
function percentage_to_utilization_color(percentage){
    if (percentage >= 90.0){
        return "#ff0e06"
    } else if (percentage >= 75.0){
        return "#ff6906"
    } else if (percentage >= 50.0){
        return "#f9e320"
    } else if (percentage >= 35.0){
        return "#00ce30"
    } else if (percentage >= 25.0){
        return "#5cd2c3"
    } else if (percentage >= 10.0){
        return "#001693"
    } else if (percentage > 0.0){
        return "#ffffff"
    } else {
        return "#646464"
    }
}

//console.time('getGraph')
d3.json(apiUrl + "/graph")
  .then(function(graph) {

    //console.timeEnd('getGraph')
    //console.time('createLinksGraph')

    var link = svg.append("g")
      .attr("id","links-g")
      .selectAll("line")
      .data(graph.links)
      .enter()
        .append("a")
        .attr("target", '_blank')
        .attr("xlink:href", function(d) { /*console.log(d);*/ return (window.location.href + '?node_a=' + d.source + "&node_b=" + d.target) })
        .append("line")
        .attr("stroke", function(d) { return percentage_to_utilization_color(d.highest_utilization) })   // # COLOR
        .attr("stroke-width", function(d) { return Math.sqrt(parseInt(d.speed) / 1000000) })  // # WIDTH
        .attr("source", function(d) { d.source })
        .attr("target", function(d) { d.target }
    );

    //console.timeEnd('createLinksGraph')

    //console.time('AddLinksEventGraph')
    link.on("click", function(event, d){
      //d3.event.preventDefault();
      //d3.event.stopPropagation();
      event.preventDefault();
      event.stopPropagation();
      OnClickLinkDetails(d.source,d.target,d.source_interfaces,d.target_interfaces);
      resize_svg_on_window_resize()
    });
    //console.timeEnd('AddLinksEventGraph')

    //console.time('AddNodesGraph')
    var node = svg.append("g")
      .attr("class", "nodes")
      .attr("id","nodes-g")
      .attr("cursor", "grab")
      .selectAll("a")
      .data(graph.nodes)
      .enter().append("a")
        .attr("target", '_blank')
        .attr("xlink:href",  function(d) { return (window.location.href + '?device=' + d.id)
    });
    //console.timeEnd('AddNodesGraph')

    //console.time('AddNodesEventGraph')
    node.on("click", function(event, d){
      event.preventDefault();
      event.stopPropagation();
      OnClickDetails(d.id);
      resize_svg_on_window_resize()
    });


    node.call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended)
    );
    //console.timeEnd('AddNodesEventGraph')

    //console.time('AddEventGraph')
    svg.call(d3.zoom()
      .extent([[0, 0], [width, height]])
      .scaleExtent([1, 8])
      .on("zoom", zoomed)
    );
    //console.timeEnd('AddEventGraph')

    //console.time('AddNodeImageGraph')
    node.append("image")
      .attr("xlink:href", function(d) { return ("img/" + d.image); })
      .attr("width", 32)
      .attr("height", 32)
      .attr("x", - 16)
      .attr("y", - 16)
      .attr("fill", function(d) { /*console.log(d.group) ; */ return color(d.group)
    });
    //console.timeEnd('AddNodeImageGraph')

    //console.time('AddNodeTextGraph')
    node.append("text")
      .attr("font-size", "1em")
      .style("fill", "#ffffff")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .attr("x", +8)
      .text(function(d) { return d.id }
    );

    node.append("title")
      .text(function(d) { return d.id; }
    );

    //console.timeEnd('AddNodeTextGraph')

    //console.time('startSimulationGraph')
    simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

    simulation.force("link")
      .links(graph.links);

    //console.timeEnd('startSimulationGraph')

    function ticked() {
      link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

      node
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"});
    }
})
.catch(function(error){
  throw error;
});


function dragstarted(event, d) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(event, d) {
  d.fx = event.x;
  d.fy = event.y;
}

function dragended(event, d) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

function zoomed(event) {
  svg.attr("transform", event.transform);
}

// ### LAST IN SCRIPT UPDATING SLIDER POSITION
// ###########################################
var elem = document.getElementById("scale_slider");
var svg_element = document.getElementById('primary-svg');
var positionInfo = svg_element.getBoundingClientRect();
elem.value = positionInfo.width;
var elem2 = document.getElementById("scale_indicator");
elem2.value = positionInfo.width;