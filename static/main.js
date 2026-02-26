function openMobileMenu() {
    const overlay = document.getElementById('mobileMenuOverlay');
    overlay.style.display = 'flex';
    overlay.style.opacity = 0;
    overlay.style.transition = 'opacity 0.3s ease-in-out';
    requestAnimationFrame(() => { overlay.style.opacity = 1; });

    const card = document.getElementById('mobileMenuCard');
    card.style.transform = 'translateY(-20px)';
    card.style.transition = 'transform 0.3s ease-in-out';
    requestAnimationFrame(() => { card.style.transform = 'translateY(0)'; });
}

function closeMobileMenu() {
    const overlay = document.getElementById('mobileMenuOverlay');
    overlay.style.opacity = 0;

    const card = document.getElementById('mobileMenuCard');
    card.style.transform = 'translateY(-20px)';

    setTimeout(() => { overlay.style.display = 'none'; }, 300);
}

document.querySelectorAll('#mobileMenuCard a').forEach(link => {
    link.addEventListener('click', closeMobileMenu);
});

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa FullCalendar
    const calendarEl = document.getElementById('calendar');
    if (calendarEl) {
        calendarEl.style.opacity = 0;
        calendarEl.style.transition = 'opacity 0.5s ease-in-out';

        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'pt-br',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: '/api/agendamentos',
            selectable: true,
            selectMirror: true,
            navLinks: true,
            editable: false,
            dayMaxEvents: true,
            height: 'auto',
            eventClick: function(info) {
                alert(`Agendamento: ${info.event.title}\nData: ${info.event.start.toLocaleDateString()}`);
            }
        });

        calendar.render();
        requestAnimationFrame(() => { calendarEl.style.opacity = 1; });

        const btnDay = document.getElementById('view-day');
        const btnWeek = document.getElementById('view-week');
        const btnMonth = document.getElementById('view-month');

        function setActive(button) {
            [btnDay, btnWeek, btnMonth].forEach(b => b.classList.remove('active'));
            button.classList.add('active');
        }

        btnDay.addEventListener('click', () => { calendar.changeView('timeGridDay'); setActive(btnDay); });
        btnWeek.addEventListener('click', () => { calendar.changeView('timeGridWeek'); setActive(btnWeek); });
        btnMonth.addEventListener('click', () => { calendar.changeView('dayGridMonth'); setActive(btnMonth); });
    }

    const formCliente = document.getElementById('form-cliente');
    if (formCliente) {
        formCliente.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(formCliente);
            const data = Object.fromEntries(formData.entries());
            try {
                const response = await fetch('/clientes', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    alert("Cliente cadastrado com sucesso!");
                    formCliente.reset();
                    const clienteSelect = document.getElementById('cliente');
                    if (clienteSelect) {
                        const option = document.createElement('option');
                        option.value = data.nome;
                        option.textContent = data.nome;
                        clienteSelect.appendChild(option);
                    }
                } else { alert("Erro ao cadastrar cliente."); }
            } catch (err) { console.error(err); alert("Erro na comunicação com o servidor."); }
        });
    }

    const formAgendamento = document.getElementById('form-agendamento');
    if (formAgendamento) {
        formAgendamento.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(formAgendamento);
            const data = Object.fromEntries(formData.entries());
            try {
                const response = await fetch('/agendar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    alert("Agendamento realizado com sucesso!");
                    formAgendamento.reset();
                } else { alert("Erro ao realizar agendamento."); }
            } catch (err) { console.error(err); alert("Erro na comunicação com o servidor."); }
        });
    }

    const lista = document.getElementById('lista-agendamentos');
    if (lista) {
        async function carregarAgendamentos() {
            try {
                const response = await fetch('/api/agendamentos');
                const agendamentos = await response.json();
                lista.innerHTML = "";
                agendamentos.forEach(ag => {
                    const item = document.createElement('li');
                    item.textContent = `${ag.nome_cliente} - ${new Date(ag.data).toLocaleString()}`;
                    lista.appendChild(item);
                });
            } catch (err) { console.error("Erro ao carregar agendamentos:", err); }
        }
        carregarAgendamentos();
    }
});
