<template>
    <div class="wrapper">
        <div class="select">选择剧本：{{ scrtptStore.scriptId }}</div>
        <Transition :mode="'out-in'" :duration="500" :enter-active-class="'animate__animated animate__fadeIn'"
                :leave-active-class="'animate__animated animate__fadeOut'">
            <RadioBtn v-show="showFlag" :name="'test'" :options="radioOptions.arr" @update="changeVal" />
        </Transition>
    </div>
</template>

<script setup lang='ts'>
import { onMounted, reactive, ref } from 'vue';
import RadioBtn from '@/components/RadioBtn.vue';
import { useScriptStore } from '@/stores/script';

const radioOptions = reactive({
    arr: []
});
const showFlag = ref(false)

const scrtptStore = useScriptStore();

const changeVal = (val: string) => {
    scrtptStore.scriptId = val;
    scrtptStore.sceneOrder = 1;
}

async function fetchData() {
    try {
        const response = await fetch('http://localhost/api/list');
        console.log(response)
        const data = await response.json();
        console.log(data)
        radioOptions.arr = data;
        showFlag.value = true
    } catch (error) {
        console.error('There was an error fetching the data:', error);
    }
}

onMounted(() => {
    fetchData()
})

</script>

<style scoped>
.select {
    height: 50px;
    width: 100%;
    text-align: center;
    align-content: center;
    font-size: 20px;
    font-weight: bolder;
    color: #dc2675;
}
</style>