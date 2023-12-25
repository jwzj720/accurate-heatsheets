<template>
    <input type="checkbox" id="todo-item" :checked="isDone" />
    <label for="todo-item">{{ label }}</label>
</template>
<script>
export default {
    props: {
        label: {required: true, type: String},
        done: {required: true, type: Boolean},
    },
    data() {
        return {
            isDone: this.done,
        }
    }
};
</script>
