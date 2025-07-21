import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserList } from './user-list/user-list';
import { UserLogin } from './user-login/user-login';
import { UserRegister } from './user-register/user-register';

const routes: Routes = [
  { path: '', component: UserList },
  { path: 'login', component: UserLogin },
  { path: 'register', component: UserRegister },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class UsersRoutingModule {}
