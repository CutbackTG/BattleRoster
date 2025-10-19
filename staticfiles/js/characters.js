// static/js/characters.js
document.addEventListener('DOMContentLoaded', function () {
  const grid = document.getElementById('char-grid');
  const newBtn = document.getElementById('new-character-btn');
  const modalEl = document.getElementById('characterModal');
  const form = document.getElementById('character-form');
  const formFields = document.getElementById('form-fields');
  const modalTitle = document.getElementById('modalTitle');
  const deleteBtn = document.getElementById('delete-btn');

  let headers = [];
  let characters = [];
  let activeChar = null; // editing

  function fetchCharacters() {
    fetch('/api/characters/')
      .then(r => r.json())
      .then(data => {
        headers = data.headers || [];
        characters = data.characters || [];
        renderGrid();
      })
      .catch(err => console.error('Failed to fetch characters:', err));
  }

  function renderGrid() {
    grid.innerHTML = '';
    characters.forEach(c => {
      const col = document.createElement('div');
      col.className = 'col-12 col-sm-6 col-md-4 col-lg-3';
      const card = document.createElement('div');
      card.className = 'card h-100';
      const img = document.createElement('img');
      img.className = 'card-img-top';
      img.alt = c.name || 'character';
      img.src = c.image_url || '/static/images/default-character.png';
      const body = document.createElement('div');
      body.className = 'card-body';
      const h5 = document.createElement('h5');
      h5.className = 'card-title';
      h5.textContent = c.name || '(No name)';
      const p = document.createElement('p');
      p.className = 'card-text';
      p.innerHTML = `<strong>HP:</strong> ${c.hp || '-'}<br><strong>MP:</strong> ${c.mp || '-'}`;
      const btnGroup = document.createElement('div');
      btnGroup.className = 'd-flex gap-2';
      const editBtn = document.createElement('button');
      editBtn.className = 'btn btn-sm btn-outline-primary';
      editBtn.textContent = 'Edit';
      editBtn.onclick = () => openModalForEdit(c);
      btnGroup.appendChild(editBtn);
      body.appendChild(h5);
      body.appendChild(p);
      body.appendChild(btnGroup);
      card.appendChild(img);
      card.appendChild(body);
      col.appendChild(card);
      grid.appendChild(col);
    });
  }

  function openModalForEdit(char) {
    activeChar = JSON.parse(JSON.stringify(char)); // clone
    modalTitle.textContent = `Edit: ${activeChar.name || 'Character'}`;
    fillForm(activeChar);
    deleteBtn.style.display = 'inline-block';
    var modal = new bootstrap.Modal(modalEl);
    modal.show();
  }

  function openModalForNew() {
    activeChar = null;
    modalTitle.textContent = 'New Character';
    fillForm({});
    deleteBtn.style.display = 'none';
    var modal = new bootstrap.Modal(modalEl);
    modal.show();
  }

  function fillForm(data) {
    formFields.innerHTML = '';
    // create inputs for each header except created/updated we may skip
    headers.forEach(h => {
      const col = document.createElement('div');
      col.className = 'col-12 col-md-6';
      const label = document.createElement('label');
      label.className = 'form-label';
      label.textContent = h;
      const input = document.createElement('input');
      input.className = 'form-control';
      input.name = h;
      input.value = data[h] || '';
      col.appendChild(label);
      col.appendChild(input);
      formFields.appendChild(col);
    });
    // hidden field for _row if editing
    const hidden = document.createElement('input');
    hidden.type = 'hidden';
    hidden.name = '_row';
    hidden.value = data._row || '';
    form.appendChild(hidden);
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    const formData = new FormData(form);
    const payload = {};
    formData.forEach((value, key) => {
      if (key === '_row') return;
      payload[key] = value;
    });
    const row = form.querySelector('input[name="_row"]').value;
    if (row) {
      // update
      payload['_row'] = parseInt(row, 10);
      fetch('/api/characters/', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(r => r.json())
        .then(() => {
          fetchCharacters();
          var m = bootstrap.Modal.getInstance(modalEl);
          m.hide();
        })
        .catch(e => console.error(e));
    } else {
      // create
      fetch('/api/characters/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(r => r.json())
        .then(() => {
          fetchCharacters();
          var m = bootstrap.Modal.getInstance(modalEl);
          m.hide();
        })
        .catch(e => console.error(e));
    }
  });

  deleteBtn.addEventListener('click', function () {
    const row = form.querySelector('input[name="_row"]').value;
    if (!row) return;
    if (!confirm('Delete this character?')) return;
    fetch('/api/characters/', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ _row: parseInt(row, 10) })
    }).then(r => r.json())
      .then(() => {
        fetchCharacters();
        var m = bootstrap.Modal.getInstance(modalEl);
        m.hide();
      }).catch(e => console.error(e));
  });

  newBtn.addEventListener('click', openModalForNew);

  // initial load
  fetchCharacters();
});

fetch("https://your-heroku-app.herokuapp.com/api/characters/")
  .then(response => response.json())
  .then(data => {
    console.log(data);
  });
