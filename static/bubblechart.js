
var diameter = 960,
    format = d3.format(",d"),
    color = d3.scaleOrdinal(d3.schemeCategory20c);

var bubble = d3.pack()
    .size([diameter, diameter])
    .padding(1.5);

var svg = d3.select("body").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .attr("class", "bubble");

d3.json("bubblechart.json", (error, data) => {
  // if (error) throw error;

  var root = d3.hierarchy(flatten(data))
      // .sort(null)
      .sum((d) => d.value);

  var node = svg.selectAll(".node")
      .data(bubble(root).leaves())
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${d.x},${d.y})`);

  node.append("title")
      .text((d) => `${d.data.className} : ${format(d.value)}`);

  node.append("circle")
      .attr("r", (d) => d.r)
      .style("fill", (d) => color(d.data.packageName));

  node.append("text")
      .attr("dy", ".3em")
      .style("text-anchor", "middle")
      .text((d) => d.data.className.substring(0, d.r / 3));
});

// Returns a flattened hierarchy containing all leaf nodes under the root.
function flatten(root) {
  var classes = [];

  function recurse(name, node) {
    if (node.children) node.children.forEach((child) => recurse(node.name, child));
    else classes.push({packageName: name, className: node.name, value: node.size});
  }

  recurse(null, root);
  return {children: classes};
}

d3.select(self.frameElement).style("height", diameter + "px");
