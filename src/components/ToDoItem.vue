<template>
    <input type="checkbox" id="todo-item" :checked="isDone" />
    <label :for="id">{{ label }}</label>
</template>
<script>

export default {
    props: {
        label: {required: true, type: String},
        done: {required: true, type: Boolean},
        id: {required: true, type: String},
    },
    data() {
        return {
            isDone: this.done,
        }
    }
};
</script>
