window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
       let datetable =  new simpleDatatables.DataTable(datatablesSimple,{
        "paging": false,
        "lengthMenu":[10],
        "info": true,
        "autoWidth":false,
        "searchable": false,
        "sortable":false,
       });
    }
});