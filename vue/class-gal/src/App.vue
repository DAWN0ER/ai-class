<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import 'animate.css/animate.css'
</script>

<template>
    <header>
        <div class="wrapper">
            <nav>
                <RouterLink to="/">Home</RouterLink>
                <RouterLink to="/paly">Replay</RouterLink>
            </nav>
        </div>
    </header>
    <div class="view">
        <Transition
        :mode="'out-in'"
        :duration="400"
        :enter-active-class="'animate__animated animate__fadeIn'"
        :leave-active-class="'animate__animated animate__fadeOut'"
        >
            <RouterView />
        </Transition>
    </div>
</template>

<style scoped>
header {
    line-height: 1.5;
    height: 90vh;
    display: flex;
    flex-direction: column;
    background-color: #F1D3CE;
    border-radius: 10px;
    padding: 10px;
    width: 10vw;
}

.wrapper{
    margin-top: 10px;
}

.view {
    max-height: 90vh;
    background-color: #F6EACB;
    width: 100%;
    padding: 5px;
    border-radius: 10px;
    padding: 10px;
}

nav {
    display: flex;
    flex-direction: column;
}

nav a{
    color: #432E54;
    text-decoration: none;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    margin-top: 10px;
}

nav a.router-link-exact-active{
    color: #AE445A;
}

nav a.router-link-exact-active:hover{
    color: #006A67;
}

nav :hover{
    color: #AE445A;
}
</style>
