google.charts.load('current', {'packages':['bar', 'line']});

google.charts.setOnLoadCallback(drawTopProductos);

$('ul.tabs').on('click', 'a', function(e) {
    var graf = $(this).data("graf")
    if (graf == "1") {
        drawTopProductos()
        //google.charts.setOnLoadCallback(drawChart1);
    }
    if (graf == "2") {
        drawTopVendedores()
        //google.charts.setOnLoadCallback(drawChart2);
    }
    if (graf == "3") {
        drawTopClientes()
        //google.charts.setOnLoadCallback(drawChart3);
    }          
});

google.charts.setOnLoadCallback(drawCiudades);
google.charts.setOnLoadCallback(drawMonto);

function drawTopClientes() {

    let jsonData = $.ajax({
        url: "/get_top_clients/",
        dataType: "json",
        async: false
        }).responseText

    let clientdata = JSON.parse(jsonData)["clientdata"]

    for (let i=0; i<clientdata.length; i++) {
        clientdata[i][1] = parseFloat(clientdata[i][1])
    }

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Cliente');
    data.addColumn('number', 'Monto Total Cotizado');
    data.addRows(clientdata)

    var options = {
        legend: {
            position: "none"
        },        
        width: 500,
        height: 200,
        bars: 'horizontal',
        isStacked: true
    };

    var chart = new google.charts.Bar(document.getElementById('top-clientes'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
} 

function drawTopVendedores() {

    let jsonData = $.ajax({
        url: "/get_top_salespersons/",
        dataType: "json",
        async: false
        }).responseText

    let salesperson = JSON.parse(jsonData)["salespersondata"]

    for (let i=0; i<salesperson.length; i++) {
        salesperson[i][1] = parseFloat(salesperson[i][1])
    }

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Vendedor');
    data.addColumn('number', 'Monto Total Cotizado');
    data.addRows(salesperson)

    var options = {
    legend: {
        position: "none"
    },
    width: 500,
    height: 200,
    bars: 'horizontal',
    isStacked: true
    };

    var chart = new google.charts.Bar(document.getElementById('top-vendedores'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
} 

function drawTopProductos() {

    let jsonData = $.ajax({
        url: "/get_top_products/",
        dataType: "json",
        async: false
        }).responseText

    let productdata = JSON.parse(jsonData)["productdata"]

    for (let i=0; i<productdata.length; i++) {
        productdata[i][1] = parseFloat(productdata[i][1])
    }

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Producto');
    data.addColumn('number', 'Monto Total Cotizado');
    data.addRows(productdata)

    var options = {

    legend: {
        position: "none"
    },
    width: 500,
    height: 200,
    bars: 'horizontal',
    //isStacked: true
    };

    var chart = new google.charts.Bar(document.getElementById('top-productos'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
}       

function drawCiudades() {

    let jsonData = $.ajax({
        url: "/get_city_data/",
        dataType: "json",
        async: false
        }).responseText
    
    console.log(jsonData)
    let citydata = JSON.parse(jsonData)["citydata"]
    
    for (let i=0; i<citydata.length; i++) {
        citydata[i][1] = parseFloat(citydata[i][1])
    }

    // for (key in citydata) {  
    //     if (key > 0) {
    //         citydata[key][1] = parseFloat(citydata[key][1])
    //     }       
    // }

    // var data = google.visualization.arrayToDataTable(citydata)

    //console.log(citydata)

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Ciudad');
    data.addColumn('number', 'Ventas');
    data.addRows(citydata)

    var options = {
        hAxis: {
            slantedText: true,
            slantedTextAngle: 90,
        },
        bar: { groupWidth: "40%" },
        series: {
            0: { color: '#e2431e' }
        },
        chart: {
        title: 'Monto Cotizado por Ciudad 2017',
        subtitle: 'en millones de pesos',
        },
        legend: {
            position: "none"
        },
        width: 300,
        height: 300,            
    };

    var chart = new google.charts.Bar(document.getElementById('monto-ciudades'));

    chart.draw(data, google.charts.Bar.convertOptions(options));
}                

function drawMonto() {

    let jsonData = $.ajax({
        url: "/get_total_month/",
        dataType: "json",
        async: false
        }).responseText
    
    let monthrows = [
        ["ene", 0],
        ["feb", 0],
        ["mar", 0],
        ["abr", 0],
        ["may", 0],
        ["jun", 0],
        ["jul", 0],
        ["ago", 0],
        ["sep", 0],
        ["oct", 0],
        ["nov", 0],
        ["dic", 0],
    ]

    let monthdata = JSON.parse(jsonData)["monthdata"]

    for (let i=0; i < monthdata.length; i++) {
        monthrows[i][1] = parseFloat(monthdata[i])
    }

    var data = new google.visualization.DataTable();
    data.addColumn('string', '2017');
    data.addColumn('number', 'Monto Total Cotizado');

    data.addRows(monthrows)

    var options = {
    chart: {
        title: 'Monto Total Cotizado 2017',
        subtitle: 'en millones de pesos'
    },
    width: 400,
    height: 300,
    legend: {
        position: "none"
    }
    };

    var chart = new google.charts.Line(document.getElementById('monto-total'));

    chart.draw(data, google.charts.Line.convertOptions(options));
}