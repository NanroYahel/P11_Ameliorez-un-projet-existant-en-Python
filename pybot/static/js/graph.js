//Code to display a graph of the requests with no result with "3D JS"


//Scale of 2 colors
var color = d3.scaleOrdinal()
			.range(["red", "green"]);

//Radius of the circle
var r = 150;

//Detemines the area for displaying graph
var canvas = d3.select(".graph").append("svg")
			.attr("width", 900)
			.attr("height", 900);

//Make group with element.
var group = canvas.append("g")
			.attr("transform", "translate(200, 200)");

//Create the arcs, with the data
var arc = d3.arc()
		.innerRadius(100)
		.outerRadius(r);

//Create a "pie" graphe with the datas : 

var pie = d3.pie()
		.value(function(d) { return d; });

var arcs = group.selectAll(".arc")
		.data(pie(data))
		.enter()
		.append("g")
		.attr("class", "arc");

arcs.append("path")
	.attr("d", arc)
	.attr("fill", function (d) { return color(d.data); });

arcs.append("text")
	.attr("transform", function(d) { return "translate("+arc.centroid(d)+")";})
	.text(function (d) { return d.data;})