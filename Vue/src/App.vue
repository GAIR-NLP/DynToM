<template>
    <div class="container">
        <h1 style="text-align: center;">Evolvable Agent in Social Scene</h1>
        <div class="unity-container">
            <UnityVue :unity="unityContext" style="width: 100%; height: 100%; border: 1px solid #000;" />
        </div>
        <div>
            <h2 style="text-align: center;">Chat</h2>
        </div>
        <div class="chat-container">
            <ul class="chat-list">
                <li v-for="message in messages" :key="message.id" class="chat-message">
                    <strong>{{ message.from_uid }}</strong> to <strong>{{ message.to_uid }}</strong>: {{ message.content
                    }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import UnityWebgl from 'unity-webgl';
import UnityVue from 'unity-webgl/vue';

const unityContext = ref(new UnityWebgl({
    loaderUrl: '/Unity/Build/Unity.loader.js',
    dataUrl: '/Unity/Build/Unity.data',
    frameworkUrl: '/Unity/Build/Unity.framework.js',
    codeUrl: '/Unity/Build/Unity.wasm',
}));

const messages = ref([
    { id: 1, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 2, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 3, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 4, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 6, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 7, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 8, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 9, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 10, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 11, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 12, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 13, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 14, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
    { id: 15, from_uid: 'A', to_uid: 'B', content: 'How are you?' },
]);

const ws = new WebSocket('ws://127.0.0.1:8080/ws');

onMounted(() => {
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        messages.value.push({
            id: messages.value.length + 1,
            from_uid: data.from_uid,
            to_uid: data.to_uid,
            content: data.content
        });
    };
});
</script>

<style>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100vw;
    overflow: auto;
}

.unity-container {
    width: 100%;
    height: 80vh;
    margin-bottom: 20px;
    border: 2px solid #ccc;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}

.chat-container {
    width: 80%;
    height: 25vh;
    background-color: #f9f9f9;
    overflow-y: auto;
    /*padding: 10px;*/
    border: 2px solid #666;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    margin-bottom: 20px;
}

.chat-list {
    list-style-type: none;
    padding: 0;
    width: 100%;
}

.chat-message {
    margin-bottom: 10px;
    padding: 5px;
    background-color: #e1e1e1;
    border-radius: 10px;
    width: fit-content;
}
</style>