import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useScriptStore = defineStore('script', () => {
    const scriptId = ref<string>('none')
    const sceneOrder = ref<number>(1)
    return { scriptId,sceneOrder }
})