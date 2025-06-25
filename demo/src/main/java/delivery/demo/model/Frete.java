package delivery.demo.model;


import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.*;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class Frete {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "cliente_id")
    @NotNull(message = "Necessário informar o cliente")
    private Cliente cliente;

    @ManyToOne
    @JoinColumn(name = "cidade_id")
    @NotNull(message = "Necessário informar a cidade")
    private Cidade cidade;

    @NotBlank(message = "A descrição deve estar preenchida")
    private String descricao;

    @NotBlank(message = "O peso deve ser preenchido")
    @Positive(message = "O peso deve ser um valor  positivo")
    private Double peso;

    @NotBlank(message = "O valor deve ser preenchido")
    @Positive(message = "O valor deve ser positivo")
    private Double valor;

    public Frete(Cliente cliente, Cidade cidade, String descricao, Double peso, Double valor) {
        this.cliente = cliente;
        this.cidade = cidade;
        this.descricao = descricao;
        this.peso = peso;
        this.valor = valor;
    }

    public Frete(Cliente cliente, Cidade cidade, String descricao, Double peso) {
        this.cliente = cliente;
        this.cidade = cidade;
        this.descricao = descricao;
        this.peso = peso;
    }
}
