<template>
    <div class="character">
        <img :src="`/cha/${img}.png`" :alt="name">
        <div class="desc">
            身份：{{ id }}
            <br>
            姓名：{{ name }}
        </div>
    </div>
</template>

<script setup lang='ts'>
import 'animate.css/animate.css'

defineProps<{
    img: string,
    name: string,
    id: string,
}>();
</script>

<style scoped>
.character {
    height: 100% -20px;
    width: 20%;
    background-color: #b4b4b880;
    padding: 10px;
    border-radius: 25px;
    backdrop-filter: blur(10px);
    border: #1F2544 2px solid;
}

.desc {
    text-align: center;
    color: #5d3b1a;
    font-size: 20px;
    font-weight: bold;
    margin-top: 10px;
    background-color: #f2efe5a4;
    border-radius: 30px;
    padding: 10px;
}

img {
    width: 100%;
    border-radius: 25px;
    margin-top: 5%;
}
</style>