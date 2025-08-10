let dashboardData = null;
let riskChart = null;
let predictionsChart = null;

const chartColors = ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545', '#D2BA4C', '#964325', '#944454', '#13343B'];

const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINT = '/api/analises/gerar_relatorio_analises/';

function apiUrl(path) {
  return `${API_BASE_URL}${path}`;
}

function formatDateBR(d = new Date()) {
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' });
}

function formatTimeBR(d = new Date()) {
  return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM carregado, iniciando aplicação...');
  loadDashboardData();
  setupRefreshButton();
  updateSystemStatus();
});

async function loadDashboardData() {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12000);

    try {
        console.log('🚀 Iniciando requisição...');
        console.log('🌐 URL completa:', apiUrl(API_ENDPOINT));

        // Teste de conectividade básica
        try {
            const healthResponse = await fetch('http://localhost:8000/', {
                method: 'GET',
                signal: controller.signal
            });
            console.log('🏥 Health check do servidor:', healthResponse.status);
        } catch (healthError) {
            console.error('❌ Servidor Django não está respondendo:', healthError);
            throw new Error('Servidor Django não está acessível');
        }

        showLoadingState();

      
        try {
            const postResponse = await fetch(apiUrl('/api/analises/analisar_todos_estudantes/'), {
                method: 'POST',
                headers: { 'Accept': 'application/json' },
                signal: controller.signal,
                cache: 'no-store'
            });
            console.log('📤 POST analisar_todos_estudantes status:', postResponse.status);
            
            if (!postResponse.ok) {
                const postErrorText = await postResponse.text();
                console.error('❌ Erro no POST:', postResponse.status, postErrorText);
                throw new Error(`Erro ao analisar estudantes: ${postResponse.status}: ${postErrorText}`);
            }
        } catch (postError) {
            console.error('❌ Erro ao fazer POST para analisar_todos_estudantes:', postError);
            throw postError;
        }

        
        const response = await fetch(apiUrl(API_ENDPOINT), {
            method: 'GET',
            headers: { 'Accept': 'application/json' },
            credentials: 'omit',
            signal: controller.signal,
            cache: 'no-store'
        });

        clearTimeout(timeout);

        console.log('📡 Status da resposta:', response.status);
        console.log('📡 Headers da resposta:', Object.fromEntries(response.headers));
        console.log('📡 URL final:', response.url);

        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Erro HTTP:', response.status, errorText);
            throw new Error(`API retornou ${response.status}: ${errorText}`);
        }

        const rawText = await response.text();
        console.log('📄 Texto bruto da resposta:', rawText);

        let data;
        try {
            data = JSON.parse(rawText);
            console.log('✅ JSON parseado com sucesso:', data);
        } catch (jsonError) {
            console.error('❌ Erro ao parsear JSON:', jsonError);
            console.error('📄 Conteúdo que causou erro:', rawText);
            throw new Error(`Resposta não é JSON válido: ${jsonError.message}`);
        }

        ensureShape(data);
        dashboardData = data;
        console.log('✅ Dados finais processados:', dashboardData);

    } catch (error) {
        console.error('❌ Erro completo:', error);
        console.error('❌ Stack trace:', error.stack);
        showErrorState(error.message);
        dashboardData = fallbackData;
        console.log('🔄 Usando dados de fallback');
    } finally {
        hideLoadingState();
        updateDashboard();
    }
}

function ensureShape(data) {
  data.mensagem ??= '';
  data.resumo_geral ??= {};
  data.distribuicao_risco ??= {};
  data.previsoes ??= {};
  data.metricas ??= {};

  data.resumo_geral.total_alunos_cadastrados ??= 0;
  data.resumo_geral.total_analises_realizadas ??= 0;
  data.resumo_geral.alunos_sem_predicao ??= 0;
  data.resumo_geral.cobertura_de_analises ??= '0%';

  data.distribuicao_risco.alto_risco ??= 0;
  data.distribuicao_risco.medio_risco ??= 0;
  data.distribuicao_risco.baixo_risco ??= 0;

  data.previsoes.evasao_prevista ??= 0;
  data.previsoes.nao_evasao_prevista ??= 0;
  data.previsoes.taxa_evasao_prevista ??= '0%';

  if (data.metricas.probabilidade_media_evasao == null) {
    data.metricas.probabilidade_media_evasao = '0';
  } else {
    data.metricas.probabilidade_media_evasao = String(data.metricas.probabilidade_media_evasao);
  }
}

function updateDashboard() {
  console.log('Atualizando dashboard com dados:', dashboardData);
  if (!dashboardData) return;

  updateMetricCards();

  setTimeout(() => {
    initializeRiskChart();
    initializePredictionsChart();
    animateProgressBar();
    setupInteractiveElements();
  }, 100);
}

function updateMetricCards() {
  if (!dashboardData) return;

  const evasaoPrevista = document.querySelector('.prediction-evasao');
  if (evasaoPrevista) evasaoPrevista.textContent = dashboardData.previsoes.evasao_prevista;

  const naoEvasaoPrevista = document.querySelector('.prediction-nao-evasao');
  if (naoEvasaoPrevista) naoEvasaoPrevista.textContent = dashboardData.previsoes.nao_evasao_prevista;
 
  const msgEl = document.querySelector('.api-message');
  if (msgEl && dashboardData.mensagem) {
    msgEl.textContent = dashboardData.mensagem;
  }

  const totalAlunos = document.querySelector('.metric-total-alunos');
  if (totalAlunos) totalAlunos.textContent = dashboardData.resumo_geral.total_alunos_cadastrados;

  const totalAnalises = document.querySelector('.metric-total-analises');
  if (totalAnalises) totalAnalises.textContent = dashboardData.resumo_geral.total_analises_realizadas;

  const alunosSemPredicao = document.querySelector('.metric-alunos-sem-predicao');
  if (alunosSemPredicao) alunosSemPredicao.textContent = dashboardData.resumo_geral.alunos_sem_predicao;

  const coberturaAnalises = document.querySelector('.metric-cobertura-analises');
  if (coberturaAnalises) coberturaAnalises.textContent = dashboardData.resumo_geral.cobertura_de_analises;

  const taxaEvasao = document.querySelector('.prediction-taxa-evasao');
  if (taxaEvasao) taxaEvasao.textContent = dashboardData.previsoes.taxa_evasao_prevista;

  const probMediaEvasao = document.querySelector('.metric-prob-media-evasao');
  if (probMediaEvasao) {
    const v = parseFloat(dashboardData.metricas.probabilidade_media_evasao);
    probMediaEvasao.textContent = isFinite(v) ? (v * 100).toFixed(1) + '%' : '-';
  }
}

function initializeRiskChart() {
  if (!dashboardData) return;

  if (riskChart) riskChart.destroy();

  const ctx = document.getElementById('riskChart');
  if (!ctx) { console.error('Elemento riskChart não encontrado'); return; }

  const chartCtx = ctx.getContext('2d');

  const data = {
    labels: ['Alto Risco', 'Médio Risco', 'Baixo Risco'],
    datasets: [{
      data: [
        dashboardData.distribuicao_risco.alto_risco,
        dashboardData.distribuicao_risco.medio_risco,
        dashboardData.distribuicao_risco.baixo_risco
      ],
      backgroundColor: ['#B4413C', '#FFC185', '#1FB8CD'],
      borderWidth: 2,
      borderColor: '#ffffff',
      hoverOffset: 10
    }]
  };

  const config = {
    type: 'doughnut',
    data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            usePointStyle: true,
            font: { size: 14, family: 'FKGroteskNeue, Inter, sans-serif' }
          }
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = context.label;
              const value = context.raw;
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
              return `${label}: ${value} aluno${value !== 1 ? 's' : ''} (${percentage}%)`;
            }
          }
        }
      },
      cutout: '60%',
      animation: { animateRotate: true, duration: 1500 }
    }
  };

  try {
    riskChart = new Chart(chartCtx, config);
  } catch (error) {
    console.error('Erro ao criar gráfico de risco:', error);
  }
}

function initializePredictionsChart() {
  if (!dashboardData) return;

  if (predictionsChart) predictionsChart.destroy();

  const ctx = document.getElementById('predictionsChart');
  if (!ctx) return;

  const chartCtx = ctx.getContext('2d');

  const data = {
    labels: ['Evasão Prevista', 'Não Evasão Prevista'],
    datasets: [{
      label: 'Número de Alunos',
      data: [
        dashboardData.previsoes.evasao_prevista,
        dashboardData.previsoes.nao_evasao_prevista
      ],
      backgroundColor: ['#B4413C', '#1FB8CD'],
      borderRadius: 6,
      borderSkipped: false
    }]
  };

  const config = {
    type: 'bar',
    data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function (context) {
              const value = context.raw;
              return `${value} aluno${value !== 1 ? 's' : ''}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
            font: { family: 'FKGroteskNeue, Inter, sans-serif' }
          },
          grid: { color: 'rgba(0, 0, 0, 0.1)' }
        },
        x: {
          ticks: { font: { family: 'FKGroteskNeue, Inter, sans-serif' } },
          grid: { display: false }
        }
      },
      animation: { duration: 1500, easing: 'easeOutQuart' }
    }
  };

  predictionsChart = new Chart(chartCtx, config);
}

function animateProgressBar() {
  if (!dashboardData) return;
  const progressFill = document.querySelector('.progress-fill');
  if (!progressFill) return;

  const v = parseFloat(dashboardData.metricas.probabilidade_media_evasao);
  const targetWidth = isFinite(v) ? v * 100 : 0;

  progressFill.style.width = '0%';
  setTimeout(() => { progressFill.style.width = targetWidth + '%'; }, 500);
}

function setupInteractiveElements() {
  const metricCards = document.querySelectorAll('.metric-card, .prediction-card');
  metricCards.forEach(card => {
    card.removeEventListener('mouseenter', handleCardHover);
    card.removeEventListener('mouseleave', handleCardLeave);
    card.addEventListener('mouseenter', handleCardHover);
    card.addEventListener('mouseleave', handleCardLeave);
  });

  const riskItems = document.querySelectorAll('.risk-item');
  riskItems.forEach(item => {
    item.removeEventListener('click', handleRiskItemClick);
    item.removeEventListener('keypress', handleRiskItemKeypress);
    item.addEventListener('click', handleRiskItemClick);
    item.addEventListener('keypress', handleRiskItemKeypress);
    item.setAttribute('tabindex', '0');
  });
}

function handleCardHover() {
  this.style.transform = 'translateY(-4px) scale(1.02)';
}
function handleCardLeave() {
  this.style.transform = 'translateY(0) scale(1)';
}
function handleRiskItemClick() {
  this.style.backgroundColor = 'var(--color-secondary)';
  setTimeout(() => { this.style.backgroundColor = 'var(--color-surface)'; }, 200);
}
function handleRiskItemKeypress(e) {
  if (e.key === 'Enter' || e.key === ' ') this.click();
}

function showLoadingState() {
  const loadingElement = document.querySelector('.loading-state');
  if (loadingElement) loadingElement.style.display = 'block';

  const dashboard = document.querySelector('.dashboard');
  if (dashboard) dashboard.classList.add('loading');
}

function hideLoadingState() {
  const loadingElement = document.querySelector('.loading-state');
  if (loadingElement) loadingElement.style.display = 'none';

  const dashboard = document.querySelector('.dashboard');
  if (dashboard) dashboard.classList.remove('loading');
}

function showErrorState(errorMessage) {
  const errorElement = document.querySelector('.error-state');
  if (errorElement) {
    errorElement.style.display = 'block';
    const errorText = errorElement.querySelector('.error-message');
    if (errorText) errorText.textContent = `Erro ao carregar dados: ${errorMessage}`;
  }
  hideLoadingState();
}

function hideErrorState() {
  const errorElement = document.querySelector('.error-state');
  if (errorElement) errorElement.style.display = 'none';
}

function setupRefreshButton() {
  const refreshButton = document.querySelector('[data-action="refresh"]');
  if (refreshButton) refreshButton.addEventListener('click', refreshData);
}

async function refreshData() {
  hideErrorState();
  await loadDashboardData();
}

function updateSystemStatus() {
  const subtitle = document.querySelector('.header__subtitle');
  if (!subtitle) return;

  const now = new Date();
  subtitle.innerHTML = `
    Análise atualizada em ${formatDateBR(now)} às ${formatTimeBR(now)} • 
    <span style="color: var(--color-success)">Sistema Ativo</span>
  `;
}

setInterval(updateSystemStatus, 30000);

setInterval(refreshData, 5 * 60 * 1000);