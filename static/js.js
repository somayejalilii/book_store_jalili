var orders;
if (localStorage.getItem('order_list') === null) {
    orders = [];
} else {
    orders = JSON.parse(localStorage.getItem('order_list'));
    for (let i = 0; i < orders.length; i++) {
        add(orders[i]);
    }
}
var show_list = document.querySelector('ul');
show_list.style.display = 'none';

var show = document.querySelector('.show')
show.addEventListener('click', function (e) {
        if (show_list.style.display == 'none') {
            show_list.style.display = 'block';
        }

    }
)

function add(title) {
    const li = document.createElement('li');
    li.className = 'list-group-item  d-flex justify-content-between';
    li.setAttribute('title', 'New Item');
    li.appendChild(document.createTextNode(title));


    const i = document  .createElement('i');
    i.className = 'close fas fa-times text-danger mr-auto delete-item';
    li.appendChild(i);
    document.querySelector('.list-group').appendChild(li);
}

document.querySelector('.add').addEventListener('click',
    function (e) {
        var task = document.querySelector('.input').value;
        tasks.push(task);
        localStorage.setItem('order_list', JSON.stringify(tasks));
        add(task);
        alert("order saved");
    }
);

var deleted = document.querySelectorAll('.close');
for (let i = 0; i < deleted.length; i++) {
    deleted[i].addEventListener('click', function (e) {
        deleted[i].parentElement.remove();
        const indexdel = orders.indexOf(deleted[i].parentElement.innerText);
        orders.splice(indexdel, 1);
        localStorage.setItem('order_list', JSON.stringify(orders));
        e.preventDefault();
    })

}

var deletall = document.querySelector('.clear-tasks');
deletall.addEventListener('click',
    function (e) {
        orders = [];
        localStorage.setItem('order_list', JSON.stringify(orders));
        show_list.innerHTML = '';
        alert("delete orders");
    }
);
