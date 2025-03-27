<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold text-center mb-8">Dashboard ANS - Análise de Sinistros</h1>
    
    <!-- Análise Anual -->
    <div class="mb-8 bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-2xl font-semibold mb-4">Análise Anual 2024</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full table-auto">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2">REG_ANS</th>
              <th class="px-4 py-2">Total de Sinistros</th>
              <th class="px-4 py-2">Trimestres Analisados</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in dadosAnuais" :key="item.reg_ans" class="border-b hover:bg-gray-50">
              <td class="px-4 py-2">{{ item.reg_ans }}</td>
              <td class="px-4 py-2 text-right">{{ item.total_sinistros }}</td>
              <td class="px-4 py-2">{{ item.trimestres }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Análise Trimestral -->
    <div class="bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-2xl font-semibold mb-4">Análise do Último Trimestre 2024</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full table-auto">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2">REG_ANS</th>
              <th class="px-4 py-2">Total de Sinistros</th>
              <th class="px-4 py-2">Meses Analisados</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in dadosTrimestre" :key="item.reg_ans" class="border-b hover:bg-gray-50">
              <td class="px-4 py-2">{{ item.reg_ans }}</td>
              <td class="px-4 py-2 text-right">{{ item.total_sinistros }}</td>
              <td class="px-4 py-2">{{ item.meses }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const dadosAnuais = ref([])
const dadosTrimestre = ref([])

const carregarDados = async () => {
  try {
    // Carregar dados anuais
    const respostaAnual = await fetch('http://localhost:5000/dados-anuais')
    dadosAnuais.value = await respostaAnual.json()

    // Carregar dados trimestrais
    const respostaTrimestral = await fetch('http://localhost:5000/dados-trimestrais')
    dadosTrimestre.value = await respostaTrimestral.json()
  } catch (erro) {
    console.error('Erro ao carregar dados:', erro)
  }
}

onMounted(() => {
  carregarDados()
})
</script>

<style scoped>
/* Add your styles here */
</style>
