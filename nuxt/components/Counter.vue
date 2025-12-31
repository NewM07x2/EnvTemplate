<template>
  <div class="space-y-4">
    <div class="text-center">
      <p class="text-4xl font-bold text-green-600 mb-4">{{ count }}</p>
      <div class="flex gap-4 justify-center">
        <button
          @click="decrement"
          class="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition"
        >
          -1
        </button>
        <button
          @click="reset"
          class="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600 transition"
        >
          リセット
        </button>
        <button
          @click="increment"
          class="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition"
        >
          +1
        </button>
      </div>
    </div>
    <p class="text-sm text-gray-500 text-center">
      このカウンターはPiniaストアを使用しています
    </p>
  </div>
</template>

<script setup lang="ts">
import { useCounterStore } from '~/stores/counter'

const counterStore = useCounterStore()
const { count } = storeToRefs(counterStore)
const { increment, decrement, reset } = counterStore
</script>
