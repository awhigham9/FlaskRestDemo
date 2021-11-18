var base = 'http://127.0.0.1:5000';
function hello() {
    console.log(`${base}/hello`);
    axios.get(`${base}/hello`)
    .then(res => console.log(res.data))
    .catch(err => console.log(err));
}

async function query() {
    var list = document.querySelector('ul');
    var title = document.querySelector('#title').value;
    await fetch(`${base}/movies/${title}`)
    .then(res => res.text())
    .then(data => {
        console.log(data);
        list.insertAdjacentHTML('afterBegin', `<li> ${data} </li>`);
    })
    .catch(err => console.log(err));
}

