<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-lg">
      <div class="container mx-auto px-4 py-4">
        <h1 class="text-3xl font-bold text-blue-600">Dashboard ANS</h1>
      </div>
    </nav>

    <div class="container mx-auto px-4 py-8">
      <!-- Resumo em Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-lg p-6 card-hover fade-in">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Total de Sinistros em 2024</h3>
          <p class="text-3xl font-bold text-blue-600">
            {{ calcularTotalSinistrosAno }}
          </p>
          <p class="text-sm text-gray-500 mt-2">Soma dos 10 maiores valores</p>
        </div>
        <div class="bg-white rounded-lg shadow-lg p-6 card-hover fade-in">
          <h3 class="text-lg font-semibold text-gray-700 mb-2">Total de Sinistros no Último Trimestre</h3>
          <p class="text-3xl font-bold text-green-600">
            {{ calcularTotalSinistrosTrimestre }}
          </p>
          <p class="text-sm text-gray-500 mt-2">Soma dos 10 maiores valores</p>
        </div>
      </div>

      <!-- Tabelas -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Dados Anuais -->
        <div class="bg-white rounded-lg shadow-lg p-6 fade-in">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-semibold text-gray-800">Maiores Sinistros em 2024</h2>
            <span class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">Anual</span>
          </div>
          
          <div v-if="carregandoAnual" class="flex justify-center items-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
          
          <div v-else-if="erro" class="bg-red-50 text-red-600 p-4 rounded">
            {{ erro }}
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="min-w-full table-hover">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Registro ANS</th>
                  <th class="px-4 py-3 text-right text-sm font-semibold text-gray-600">Total de Sinistros</th>
                  <th class="px-4 py-3 text-center text-sm font-semibold text-gray-600">Trimestres</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="(item, index) in dadosAnuais" :key="item.reg_ans" 
                    class="hover:bg-gray-50 transition-colors"
                    :class="{'bg-blue-50': index < 3}">
                  <td class="px-4 py-3 text-sm">{{ item.reg_ans }}</td>
                  <td class="px-4 py-3 text-right text-sm font-medium" 
                      :class="{'text-blue-600': index < 3}">
                    {{ item.total_sinistros }}
                  </td>
                  <td class="px-4 py-3 text-center text-sm text-gray-500">
                    {{ item.trimestres.join(', ') }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Dados do Último Trimestre -->
        <div class="bg-white rounded-lg shadow-lg p-6 fade-in">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-semibold text-gray-800">Maiores Sinistros no Último Trimestre</h2>
            <span class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">Trimestral</span>
          </div>
          
          <div v-if="carregandoTrimestre" class="flex justify-center items-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
          </div>
          
          <div v-else-if="erroTrimestre" class="bg-red-50 text-red-600 p-4 rounded">
            {{ erroTrimestre }}
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="min-w-full table-hover">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Registro ANS</th>
                  <th class="px-4 py-3 text-right text-sm font-semibold text-gray-600">Total de Sinistros</th>
                  <th class="px-4 py-3 text-center text-sm font-semibold text-gray-600">Mês</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="(item, index) in dadosTrimestre" :key="item.reg_ans" 
                    class="hover:bg-gray-50 transition-colors"
                    :class="{'bg-green-50': index < 3}">
                  <td class="px-4 py-3 text-sm">{{ item.reg_ans }}</td>
                  <td class="px-4 py-3 text-right text-sm font-medium"
                      :class="{'text-green-600': index < 3}">
                    {{ item.total_sinistros }}
                  </td>
                  <td class="px-4 py-3 text-center text-sm text-gray-500">
                    {{ item.meses.join(', ') }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const dadosAnuais = ref([])
    const dadosTrimestre = ref([])
    const carregandoAnual = ref(true)
    const carregandoTrimestre = ref(true)
    const erro = ref(null)
    const erroTrimestre = ref(null)

    // Computar totais
    const calcularTotalSinistrosAno = computed(() => {
      if (!dadosAnuais.value.length) return 'Carregando...'
      const total = dadosAnuais.value.reduce((acc, curr) => {
        const valor = parseFloat(curr.total_sinistros.replace(/[^\d,]/g, '').replace(',', '.'))
        return acc + valor
      }, 0)
      return `R$ ${total.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
    })

    const calcularTotalSinistrosTrimestre = computed(() => {
      if (!dadosTrimestre.value.length) return 'Carregando...'
      const total = dadosTrimestre.value.reduce((acc, curr) => {
        const valor = parseFloat(curr.total_sinistros.replace(/[^\d,]/g, '').replace(',', '.'))
        return acc + valor
      }, 0)
      return `R$ ${total.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
    })

    // Função para carregar os dados
    const carregarDados = async () => {
      try {
        carregandoAnual.value = true
        erro.value = null

        const resposta = await fetch('http://127.0.0.1:5000/api/top-operadoras/ano')
        if (!resposta.ok) throw new Error('Erro ao carregar dados')
        const dados = await resposta.json()
        
        dadosAnuais.value = dados.data.map(item => ({
          reg_ans: item.reg_ans,
          total_sinistros: item.total_sinistros_formatado,
          trimestres: item.trimestres
        }))

      } catch (e) {
        erro.value = `Erro ao carregar dados: ${e.message}`
        console.error('Erro:', e)
      } finally {
        carregandoAnual.value = false
      }
    }

    const carregarDadosTrimestre = async () => {
      try {
        carregandoTrimestre.value = true
        erroTrimestre.value = null

        const respostaTrimestre = await fetch('http://127.0.0.1:5000/api/top-operadoras/trimestre')
        if (!respostaTrimestre.ok) throw new Error('Erro ao carregar dados do trimestre')
        const dadosTrimestreResponse = await respostaTrimestre.json()
        
        dadosTrimestre.value = dadosTrimestreResponse.data.map(item => ({
          reg_ans: item.reg_ans,
          total_sinistros: item.total_sinistros_formatado,
          meses: item.meses
        }))

      } catch (e) {
        erroTrimestre.value = `Erro ao carregar dados: ${e.message}`
        console.error('Erro:', e)
      } finally {
        carregandoTrimestre.value = false
      }
    }

    // Carregar dados quando o componente for montado
    onMounted(() => {
      carregarDados()
      carregarDadosTrimestre()
    })

    return {
      dadosAnuais,
      dadosTrimestre,
      carregandoAnual,
      carregandoTrimestre,
      erro,
      erroTrimestre,
      calcularTotalSinistrosAno,
      calcularTotalSinistrosTrimestre
    }
  }
}
</script>