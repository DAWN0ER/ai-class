<template>
    <div class="contain">
        <div class="stage-wrapper">
            <Transition :mode="'out-in'" :duration="500" :enter-active-class="'animate__animated animate__fadeIn'"
                :leave-active-class="'animate__animated animate__fadeOut'">
                <Conversation v-if="scene === 'conversation'" :left-one="conversationData.talkerL"
                    :right-one="conversationData.talkerR" />
                <Broadcast v-else-if="scene === 'broadcast'" :teacher-name="broadcastData.teacherName"
                    :teacher-msg="broadcastData.teacherMsg" :teacher-img="broadcastData.teacherImg"
                    :student-msg-list="broadcastData.studentList" />
                <div v-else></div>
            </Transition>
        </div>
        <div class="console-wrapper">
            <div v-show="timerId !== 0" class="desc">Auto Playing...</div>
            <Transition :mode="'out-in'" :enter-active-class="'animate__animated animate__bounceIn'"
                :leave-active-class="'animate__animated animate__bounceOut'">
                <div :key="scene" class="desc">{{ scene }}</div>
            </Transition>
            <Transition :mode="'out-in'" :enter-active-class="'animate__animated animate__bounceIn'"
                :leave-active-class="'animate__animated animate__bounceOut'">
                <div :key="order" class="desc">SCENE-{{ order }}</div>
            </Transition>
            <div class="desc">{{ scriptStore.scriptId }}</div>
            <IconSelector @click="last" :icon="'last'" />
            <IconSelector @click="play" :icon="'play'" />
            <IconSelector @click="next" :icon="'next'" />
            <IconSelector @click="stop" :icon="'stop'" />
            <IconSelector @click="reset" :icon="'reset'" />
        </div>
    </div>
</template>

<script setup lang='ts'>
import IconSelector from '@/components/IconSelector.vue';
import Conversation, { type Talker } from '@/components/Conversation.vue';
import Broadcast from '@/components/Broadcast.vue';

import 'animate.css/animate.css'
import { onMounted, reactive, ref } from 'vue';
import { useScriptStore } from '@/stores/script';

const scene = ref("default")
const order = ref(1)
const timerId = ref(0);

const scriptStore = useScriptStore();
const conversationData = reactive({
    talkerL: {} as Talker,
    talkerR: {} as Talker,
})
const broadcastData = reactive({
    teacherName: '',
    teacherImg: '',
    teacherMsg: '',
    studentList: [],
})

async function fetchData(scriptV: string, orderV: number) {
    const queryString = new URLSearchParams({
        script: scriptV,
        order: orderV.toString()
    }).toString();
    try {
        const response = await fetch(`http://localhost:12344/api/get?${queryString}`);
        const data = await response.json();
        if (data.scene === "conversation") {
            conversationData.talkerL = data.talkerL as Talker;
            conversationData.talkerR = data.talkerR as Talker;
        } else if (data.scene === "broadcast") {
            broadcastData.teacherImg = data.teacher.img
            broadcastData.teacherName = data.teacher.name
            broadcastData.teacherMsg = data.teacher.msg
            broadcastData.studentList = data.students
        }
        scriptStore.sceneOrder = data.order
        scene.value = data.scene
        order.value = data.order
    } catch (error) {
        console.error('There was an error fetching the data:', error);
    }
}

onMounted(() => {
    if(scriptStore.scriptId !== 'none'){
        fetchData(scriptStore.scriptId, scriptStore.sceneOrder)
    }
})

const next = () => {
    fetchData(scriptStore.scriptId, scriptStore.sceneOrder + 1)
}

const last = () => {
    if (scriptStore.sceneOrder <= 1)
        return;
    fetchData(scriptStore.scriptId, scriptStore.sceneOrder - 1)
}

const play = () => {
    timerId.value = setInterval(() => {
        const o1 = scriptStore.sceneOrder
        fetchData(scriptStore.scriptId, scriptStore.sceneOrder + 1)
            .then(() => {
                if (o1 === scriptStore.sceneOrder) {
                    clearInterval(timerId.value)
                    timerId.value = 0;
                }
            })
    }, 3000) // 3s 一次
}

const stop = () => {
    if (timerId.value !== 0) {
        clearInterval(timerId.value)
        timerId.value = 0
    }
}

const reset = () => {
    fetchData(scriptStore.scriptId,1)
}

</script>

<style scoped>
.stage-wrapper {
    max-height: 85%;
    height: 85%;
    width: 100%;
    background-image: url('classroom.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    border-radius: 25px;

}

.console-wrapper {
    height: 10%;
    width: 100%-20px;
    padding-right: 20px;
    align-items: center;
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
}

.desc {
    height: 32px;
    text-align: center;
    align-content: center;
    margin-right: 15px;
    border-radius: 10px;
    background-color: cadetblue;
    padding-left: 10px;
    padding-right: 10px;
    color: floralwhite;
    font-size: 20px;
    font-weight: bold;
}

.contain {
    height: 100%;
    width: 100%;
    max-height: 90vh;
}
</style>