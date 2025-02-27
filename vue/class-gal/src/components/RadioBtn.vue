<template>
    <div class="wrapper">
        <div v-for="opt in options" class="btn" @click="test = opt">
            {{ opt }}
        </div>
    </div>
</template>

<script setup lang='ts'>
import { ref, toRefs, watch } from 'vue';


const props = defineProps<{
    options: string[]
}>()

const { options } = toRefs(props);

const emit = defineEmits(['update'])

const test = ref(options.value[0]);

watch(test, (newVal) => {
    emit('update', newVal)
})

</script>

<style scoped>
.wrapper {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    width: 100% - 20px;
    max-height: 70vh;
    grid-gap: 25px;
    overflow-y: auto;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.btn {
    height: 50px;
    width: 200px;
    cursor: pointer;
    background-color: rgb(135, 168, 235, 0.5);
    text-align: center;
    align-content: center;
    border-radius: 15px;
    transition: transform 0.2s ease;
    backdrop-filter: blur(10px);
    /* 毛玻璃效果 */
}

.btn:hover {
    transform: scale(1.1);
    cursor: pointer;
    box-shadow: 0 8px 17px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    /* 鼠标悬浮时的阴影效果 */
}
</style>