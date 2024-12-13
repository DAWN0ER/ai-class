<template>
    <div class="chat-bubble-container">
        <div :class="['chat-bubble', `chat-bubble-${type}`]">
            <div v-html="md" :class="['markdown-body', 'chat-bubble-content']">
            </div>
        </div>
    </div>
</template>

<script setup lang='ts'>
import 'github-markdown-css/github-markdown-dark.css'
import { Marked } from 'marked';
import { ref, toRefs, watch } from 'vue';

const props = defineProps<{
    msg: string,
    type: string,
}>()
const { msg, type } = toRefs(props)

const marked = new Marked()
const md = ref(marked.parse(props.msg) as string);

watch(msg, (newV, oldV) => {
    md.value = marked.parse(newV) as string
})

</script>

<style>
.chat-bubble-container {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    margin-bottom: 10px;
}

.chat-bubble {
    max-width: 85%;
    padding: 8px 12px;
    border-radius: 14px;
    background-color: #e6e6e6;
    margin-bottom: 4px;
    word-wrap: break-word;
    box-shadow: 0 5px 5px 0 rgba(0, 0, 0, 0.2), 0 7px 7px 0 rgba(0, 0, 0, 0.19);
}

.chat-bubble-content {
    font-size: 16px;
    line-height: 1.5;
    background-color: transparent !important;
}

.chat-bubble-content blockquote {
    color: white !important;
}

.chat-bubble-content h1,
h2,
h3,
h4,
h5,
h6 {
    margin-top: 2px !important;
    padding-bottom: 0 !important;
}

.chat-bubble-content * {
    margin-bottom: 5px !important;
}

/* 靠右边的消息样式 */
.chat-bubble-R {
    background-color: #006cbe;
    color: white;
    align-self: flex-end;
}

/* 靠左边的消息样式 */
.chat-bubble-L {
    background-color: #00a80e;
    color: white;
    align-self: flex-start;
}
</style>