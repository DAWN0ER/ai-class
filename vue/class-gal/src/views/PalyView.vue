<template>
    <div class="contain">
        <div class="stage-wrapper">
            <Transition :mode="'out-in'" :duration="500" :enter-active-class="'animate__animated animate__fadeIn'"
                :leave-active-class="'animate__animated animate__fadeOut'">
                <Conversation v-if="scene === 'conversation'" :left-one="conversationData.talkerL"
                    :right-one="conversationData.talkerR" />
                <Broadcast v-else-if="scene === 'broadcast'" :speakerName="broadcastData.speakerName"
                    :speakerMsg="broadcastData.speakerMsg" :speakerImg="broadcastData.speakerImg"
                    :speaker-id="broadcastData.speakerId" :student-msg-list="broadcastData.studentList" />
                <div v-else></div>
            </Transition>
        </div>
        <div class="console-wrapper">
            <Transition :mode="'out-in'" :enter-active-class="'animate__animated animate__bounceIn'"
                :leave-active-class="'animate__animated animate__bounceOut'">
                <div v-show="timerId !== 0" class="desc">Auto Playing...</div>
            </Transition>
            <div class="desc">{{ scriptStore.scriptId }}</div>
            <div @click="jump" :class="['desc', 'click-desc']">SCENE<input @click.stop v-model="order"
                    class="console-input" /></div>
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
    speakerName: '',
    speakerImg: '',
    speakerMsg: '',
    speakerId: '',
    studentList: [],
})

async function fetchData(scriptV: string, orderV: number) {
    const queryString = new URLSearchParams({
        script: scriptV,
        order: orderV.toString()
    }).toString();
    try {
        const response = await fetch(`http://localhost/api/get?${queryString}`);
        const data = await response.json();
        if (data.scene === "conversation") {
            conversationData.talkerL = data.talkerL as Talker;
            conversationData.talkerR = data.talkerR as Talker;
        } else if (data.scene === "broadcast") {
            broadcastData.speakerImg = data.speaker.img
            broadcastData.speakerName = data.speaker.name
            broadcastData.speakerMsg = data.speaker.msg
            broadcastData.speakerId = data.speaker.id
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
    if (scriptStore.scriptId !== 'none') {
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
    fetchData(scriptStore.scriptId, scriptStore.sceneOrder + 1)
    timerId.value = setInterval(() => {
        const o1 = scriptStore.sceneOrder
        fetchData(scriptStore.scriptId, scriptStore.sceneOrder + 1)
            .then(() => {
                if (o1 === scriptStore.sceneOrder) {
                    clearInterval(timerId.value)
                    timerId.value = 0;
                }
            })
    }, 5000) // 5s 一次
}

const stop = () => {
    if (timerId.value !== 0) {
        clearInterval(timerId.value)
        timerId.value = 0
    }
}

const reset = () => {
    fetchData(scriptStore.scriptId, 1)
}

const jump =() =>{
    fetchData(scriptStore.scriptId, order.value)
}

</script>

<style scoped>
.stage-wrapper {
    max-height: 85%;
    height: 85%;
    width: 100%;
    background-image: url('/classroom.png');
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
    display: flex;
    height: 32px;
    text-align: center;
    align-content: center;
    align-items: center;
    margin-right: 15px;
    border-radius: 10px;
    background-color: cadetblue;
    padding-left: 10px;
    padding-right: 10px;
    color: floralwhite;
    font-size: 20px;
    font-weight: bold;
}

.click-desc:hover {
    color: #FFCCE1;
    cursor: pointer;
}

.contain {
    height: 100%;
    width: 100%;
    max-height: 90vh;
}

.console-input {
    outline-style: none;
    border: 3px solid #CBD2A4;
    border-radius: 3px;
    height: 20px;
    width: 32px;
    text-align: center;
    font-size: 16px;
    transition: border-color 0.3s;
    margin-left: 5px;
    font-weight: bolder;
    background-color: whitesmoke;
    color: #4B5945;
}

.console-input:focus {
    border-color: #DA8359;
}
</style>