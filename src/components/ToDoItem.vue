<template>
    <input type="checkbox" id="todo-item" :checked="isDone" />
    <label :for="id">{{ label }}</label>
</template>
<script>
import uniqueId from "lodash.uniqueid";
export default {
    props: {
        label: {required: true, type: String},
        done: {required: true, type: Boolean},
    },
    data() {
        return {
            isDone: this.done,
            id: uniqueId("todo-"),
        }
    }
};
</script>
