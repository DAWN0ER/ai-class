<template>
    <div class="wrapper">
        <Transition :mode="'out-in'" :duration="{ enter: 1000, leave: 500 }"
            :enter-active-class="'animate__animated animate__backInLeft'"
            :leave-active-class="'animate__animated animate__backOutLeft'">
            <Character :key="speakerName" :id="speakerId" :name="speakerName" :img="speakerImg" />
        </Transition>
        <div class="chat">
            <div class="teacher-chat">
                <Transition :mode="'out-in'" :duration="{ enter: 1000, leave: 500 }"
                    :enter-active-class="'animate__animated animate__bounceInLeft'"
                    :leave-active-class="'animate__animated animate__backOutLeft'">
                    <Box :key="speakerMsg" v-if="speakerMsg !== ''" :msg="speakerMsg" :type="'L'" />
                </Transition>
            </div>
            <Transition :mode="'out-in'" :duration="{ enter: 800, leave: 800 }"
                :enter-active-class="'animate__animated animate__bounceIn'"
                :leave-active-class="'animate__animated animate__bounceOut'">
                <div class="rolling-chat" :key="speakerId+speakerMsg">
                    <div v-for="std in studentMsgList" class="a-chat">
                        <div class="chat-wrapper">
                            <Box :msg="std.msg" :type="'R'" />
                        </div>
                        <div class="desc-card">
                            <img class="avater" :src="`/cha/${std.img}.png`">
                            <div class="name-card">
                                {{ std.name }}
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>
        </div>
    </div>
</template>

<script setup lang='ts'>
import Box from './Box.vue';
import Character from './Character.vue';

export interface RollingLine {
    msg: string,
    name: string,
    img: string,
}

defineProps<{
    speakerName: string,
    speakerMsg: string,
    speakerImg: string,
    speakerId: string,
    studentMsgList: RollingLine[],
}>();

</script>

<style scoped>
.wrapper {
    height: 100%;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
}

.chat {
    width: 80%;
    background-color: #e5e1daa4;
    display: flex;
    flex-direction: column;
    border-radius: 25px;
    backdrop-filter: blur(5px);
}

.teacher-chat {
    height: 25%;
    padding: 20px;
    padding-bottom: 0px;
    overflow-y: auto;
    overflow-x: hidden;
    border-bottom: 3px solid #3C5B6Fb6;
    border-radius: 1px;
}

.rolling-chat {
    height: 75%;
    padding: 10px;
    padding-bottom: 0px;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    overflow-x: hidden;
}

.a-chat {
    max-height: 200px;
    margin-bottom: 10px;
    display: flex;
    flex-direction: row;
}

.chat-wrapper {
    width: 80%;
    max-height: 100%;
    overflow-y: auto;
    padding-right: 10px;
}

.desc-card {
    width: 20%;
    max-height: 100%;
    max-width: 190px;
    overflow: hidden;
    border-radius: 20%;
    position: relative;
}

.avater {
    width: 100%;
    height: auto;
    object-fit: contain;
    object-position: top;
}

.name-card {
    position: absolute;
    width: 80%;
    top: 70%;
    left: 50%;
    padding: 5px;
    transform: translate(-50%, 0);
    text-align: center;
    border-radius: 20px;
    font-size: 20px;
    font-weight: bold;
    background-color: #4b5945e8;
    color: #E5E3D4;
}
</style>