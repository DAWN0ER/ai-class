<template>
    <div class="wrapper">
        <Transition :mode="'out-in'" :duration="{enter:1000,leave:500}" :enter-active-class="'animate__animated animate__backInLeft'"
            :leave-active-class="'animate__animated animate__backOutLeft'">
            <Character :key="leftOne.name" :img="leftOne.img" :name="leftOne.name" :id="leftOne.id" />
        </Transition>
        <div class="chat">
            <Transition :mode="'out-in'" :duration="{enter:1000,leave:500}" :enter-active-class="'animate__animated animate__bounceInLeft'"
                :leave-active-class="'animate__animated animate__backOutLeft'">
                <Box v-if="leftOne.msg !== ''" :key="leftOne.msg" :msg="leftOne.msg" :type="'L'" />
                <div v-else></div>
            </Transition>
            <Transition :mode="'out-in'" :duration="{enter:1000,leave:500}" :enter-active-class="'animate__animated animate__bounceInRight'"
                :leave-active-class="'animate__animated animate__backOutRight'">
                <Box v-if="rightOne.msg !== ''" :key="rightOne.msg" :msg="rightOne.msg" :type="'R'" />
                <div v-else></div>
            </Transition>
        </div>
        <Transition :mode="'out-in'" :duration="{enter:1000,leave:500}" :enter-active-class="'animate__animated animate__backInRight'"
            :leave-active-class="'animate__animated animate__backOutRight'">
            <Character :key="rightOne.name" :img="rightOne.img" :name="rightOne.name" :id="rightOne.id" />
        </Transition>
    </div>
</template>

<script setup lang='ts'>
import Box from '@/components/Box.vue';
import Character from '@/components/Character.vue';
import 'animate.css/animate.css'
import { toRefs } from 'vue';

export interface Talker {
    img: string,
    name: string,
    id: string,
    msg: string,
}

const props = defineProps<{
    leftOne: Talker,
    rightOne: Talker,
}>()

let { leftOne, rightOne } = toRefs(props)

</script>

<style scoped>
.wrapper {
    height: 100%;
    display: flex;
    flex-direction: row;
}

.chat {
    height: 100% - 30px;
    width: 60%;
    overflow: auto;
    overflow-x: hidden;
    padding-top: 15px;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 15px;
    background-color: rgba(255, 250, 240, 0.5);
    backdrop-filter: blur(10px);
    border-bottom: 3px solid #392467;
    border-top: 3px solid #392467;
}

</style>