/* Dibuja el arbol de decision con D3 y resalta la ruta activa. */
(function () {
    const data = window.TREE_DATA;
    const svgEl = document.getElementById("tree-svg");
    if (!data || !svgEl || typeof d3 === "undefined") {
        return;
    }

    const activos = new Set((window.ACTIVE_PATH || []).map(Number));
    const width = 1000;
    const height = 520;

    const svg = d3.select("#tree-svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("preserveAspectRatio", "xMidYMid meet");

    const g = svg.append("g");
    const zoom = d3.zoom()
        .scaleExtent([0.3, 2.5])
        .on("zoom", (event) => g.attr("transform", event.transform));
    svg.call(zoom);
    svg.call(zoom.transform,
        d3.zoomIdentity.translate(60, height / 2));

    const layout = d3.tree().nodeSize([34, 165]);
    const root = d3.hierarchy(data, (d) => d.children || []);
    const porId = new Map();
    root.each((d) => porId.set(d.data.id, d));

    // Plegar todo salvo los ancestros de la ruta activa.
    root.each((d) => {
        d._children = d.children;
        if (d.depth >= 1) {
            d.children = null;
        }
    });
    const expandirAncestros = (id) => {
        let nodo = porId.get(id);
        let cur = nodo ? nodo.parent : null;
        while (cur) {
            if (!cur.children && cur._children) {
                cur.children = cur._children;
            }
            cur = cur.parent;
        }
    };
    activos.forEach(expandirAncestros);

    let i = 0;
    const duracion = 300;

    function etiqueta(d) {
        const n = d.data;
        if (n.truncated) {
            return "\u2026";
        }
        if (n.is_leaf) {
            return "\u2192 " + (n.label === null ? "?" : n.label);
        }
        return n.feature + " \u2264 " + n.threshold;
    }

    function color(d) {
        if (activos.has(d.data.id)) {
            return "#f59e0b";
        }
        if (d.data.truncated) {
            return "#cbd5e1";
        }
        if (d.data.is_leaf) {
            return "#16a34a";
        }
        return "#2563eb";
    }

    function update(source) {
        layout(root);
        const nodos = root.descendants();
        const enlaces = root.links();

        nodos.forEach((d) => {
            d.y = d.depth * 165;
        });

        const node = g.selectAll("g.node")
            .data(nodos, (d) => d.data.id);
        const nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .attr("transform", () => "translate("
                + source.y0 + "," + source.x0 + ")")
            .style("cursor", "pointer")
            .on("click", (event, d) => {
                if (d.data.truncated) {
                    return;
                }
                if (d.children || (d._children && d._children.length)) {
                    d.children = d.children ? null : d._children;
                    update(d);
                }
            });

        nodeEnter.append("circle")
            .attr("r", 1)
            .attr("fill", "#fff")
            .attr("stroke-width", 2);

        nodeEnter.append("text")
            .attr("class", "tree-label")
            .attr("dy", "0.32em")
            .attr("text-anchor", "middle");

        nodeEnter.append("title");

        const nodeMerge = nodeEnter.merge(node);
        nodeMerge.transition().duration(duracion)
            .attr("transform", (d) => "translate(" + d.y + "," + d.x + ")");
        nodeMerge.select("circle")
            .attr("r", 15)
            .attr("stroke", color)
            .attr("class", (d) => activos.has(d.data.id) ? "pulse" : "");
        nodeMerge.select("text")
            .text(etiqueta)
            .attr("fill", (d) => activos.has(d.data.id) ? "#b45309" : "#1f2937");
        nodeMerge.select("title")
            .text((d) => "nodo " + d.data.id + " | muestras "
                + d.data.samples);

        node.exit().transition().duration(duracion)
            .attr("transform", () => "translate(" + source.y + ","
                + source.x + ")")
            .style("opacity", 0)
            .remove();

        const link = g.selectAll("path.link")
            .data(enlaces, (d) => d.target.data.id);
        const linkEnter = link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", () => {
                const o = { x: source.x0, y: source.y0 };
                return diagonal(o, o);
            });
        linkEnter.merge(link).transition().duration(duracion)
            .attr("d", (d) => diagonal(d.source, d.target))
            .attr("stroke", (d) => activos.has(d.target.data.id)
                ? "#f59e0b" : "#cbd5e1")
            .attr("stroke-width", (d) => activos.has(d.target.data.id)
                ? 2.5 : 1.5);
        link.exit().transition().duration(duracion)
            .attr("d", () => {
                const o = { x: source.x, y: source.y };
                return diagonal(o, o);
            })
            .style("opacity", 0)
            .remove();

        nodos.forEach((d) => {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }

    function diagonal(s, d) {
        return "M " + s.y + " " + s.x
            + " C " + ((s.y + d.y) / 2) + " " + s.x
            + " " + ((s.y + d.y) / 2) + " " + d.x
            + " " + d.y + " " + d.x;
    }

    root.x0 = height / 2;
    root.y0 = 0;
    update(root);
})();
