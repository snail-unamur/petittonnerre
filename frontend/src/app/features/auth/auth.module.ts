import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { ReactiveFormsModule } from "@angular/forms";
import { RouterModule } from "@angular/router";
import { RegisterComponent } from "./register.component";

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RegisterComponent,
    RouterModule.forChild([{ path: "register", component: RegisterComponent }]),
  ],
})
export class AuthModule {}
