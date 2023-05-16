# PetShop

## Description

API using Django Rest FrameWork that allowed the pet shop to have greater control and organization of animal data.

## Endpoints

| HTTP Method | Description   | Endpoint             |
| ----------- | ------------- | -------------------- |
| POST        | Register pet  | `/api/pet/`          |
| GET         | List pets     | `/api/pet/`          |
| GET         | Fiter per pet | `/api/pet/<pet_id>/` |
| PATCH       | Update pet    | `/api/pet/<pet_id>/` |
| DELETE      | Delete pet    | `/api/pet/<pet_id>/` |

## Run the tests for each task

Example:

- Task 1

```shell
pytest --testdox -vvs tests/tarefas/tarefa_1/
```

- Task 2

```shell
pytest --testdox -vvs tests/tarefas/tarefa_2/
```

- Task 3

```shell
pytest --testdox -vvs tests/tarefas/tarefa_3/
```
