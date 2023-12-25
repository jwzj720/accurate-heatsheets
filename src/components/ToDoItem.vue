<template>
    <input type="checkbox" id="todo-item" />
    <label for="todo-item">{{ label }}</label>
</template>
<script>
export default {
    props: {
        label: {required: true, type: String},
        done: {required: true, type: Boolean},
    },
};
</script>
